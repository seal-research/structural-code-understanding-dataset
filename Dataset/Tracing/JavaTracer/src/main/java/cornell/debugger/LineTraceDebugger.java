package cornell.debugger;

import com.sun.jdi.*;
import com.sun.jdi.connect.AttachingConnector;
import com.sun.jdi.connect.Connector;
import com.sun.jdi.event.*;
import com.sun.jdi.request.*;
import com.sun.jdi.AbsentInformationException;

import java.util.Map;

import java.util.ArrayList;
import java.util.List;



public class LineTraceDebugger {
    private static final List<Integer> executedLines = new ArrayList<>();

    public static void main(String[] args) {
        try {
            VirtualMachine vm = connectToJVM("localhost", "5005");
            
            EventRequestManager erm = vm.eventRequestManager();
            ClassPrepareRequest classPrepareRequest = erm.createClassPrepareRequest();
            classPrepareRequest.addClassFilter("cornell.debugger.*");
            classPrepareRequest.enable();

            ThreadReference mainThread = null;
            while (mainThread == null) {
                for (ThreadReference thread : vm.allThreads()) {
                    if ("main".equals(thread.name())) {
                        mainThread = thread;
                        break;
                    }
                }
                Thread.sleep(100);
            }

            StepRequest stepRequest = erm.createStepRequest(mainThread, StepRequest.STEP_LINE, StepRequest.STEP_INTO);
            stepRequest.addClassFilter("cornell.debugger.*");
            stepRequest.enable();

            System.out.println("Debugger attached and waiting for events...");

            EventQueue eventQueue = vm.eventQueue();
            while (true) {
                EventSet eventSet = eventQueue.remove();
                for (Event event : eventSet) {
                    if (event instanceof ClassPrepareEvent) {
                        ClassPrepareEvent cpe = (ClassPrepareEvent) event;
                        ReferenceType refType = cpe.referenceType();
                        System.out.println("Class loaded: " + refType.name());
                        setupLineTrace(erm, refType);
                    } 
                    else if (event instanceof StepEvent) {
                        StepEvent se = (StepEvent) event;
                        Location loc = se.location();
                        String className = loc.declaringType().name();
                        
                        if (className.startsWith("cornell.debugger")) {
                            // Get the method's bytecodes
                            Method method = loc.method();
                            byte[] bytecodes = method.bytecodes();
                            long index = loc.codeIndex();
                            
                            // Check if this location is just a closing brace
                            if (index >= 0 && index < bytecodes.length) {
                                byte instruction = bytecodes[(int)index];
                                // Skip closing bracket (implicit return statement)
                                executedLines.add(loc.lineNumber());
                                System.out.println("Executed line: " + loc.lineNumber());
                            }
                        }
                    }
                    else if (event instanceof VMDeathEvent || event instanceof VMDisconnectEvent) {
                        System.out.println("Application terminated");
                        System.out.println("Executed lines in order: " + executedLines);
                        return;
                    }
                }
                eventSet.resume();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static VirtualMachine connectToJVM(String host, String port) throws Exception {
        VirtualMachineManager vmm = Bootstrap.virtualMachineManager();
        AttachingConnector connector = vmm.attachingConnectors()
            .stream()
            .filter(c -> c.transport().name().equals("dt_socket"))
            .findFirst()
            .orElseThrow(() -> new RuntimeException("No socket transport found"));

        Map<String, Connector.Argument> args = connector.defaultArguments();
        args.get("hostname").setValue(host);
        args.get("port").setValue(port);

        return connector.attach(args);
    }

    private static void setupLineTrace(EventRequestManager erm, ReferenceType refType) {
        try {
            for (Location loc : refType.allLineLocations()) {
                Method method = loc.method();
                byte[] bytecodes = method.bytecodes();
                long index = loc.codeIndex();
                
                // Set breakpoints for all lines except those that only contain return instructions
                if (index >= 0 && index < bytecodes.length) {
                    byte instruction = bytecodes[(int)index];
                    if (!(instruction == (byte)0xb1 || instruction == (byte)0xb0) || 
                        (index > 0 && bytecodes[(int)index-1] != (byte)0)) {
                        BreakpointRequest bpReq = erm.createBreakpointRequest(loc);
                        bpReq.enable();
                    }
                }
            }
            System.out.println("Set breakpoints for all executable lines in " + refType.name());
        } catch (AbsentInformationException e) {
            System.err.println("Could not set breakpoints for " + refType.name() + ": " + e.getMessage());
        }
    }
}