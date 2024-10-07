void bubbleSort(int arr[], int n) { //1
    for (int i = 0; i < n - 1; i++) //2
        for (int j = 0; j < n - i - 1; j++) //3
            if (arr[j] > arr[j + 1]) //4
                std::swap(arr[j], arr[j + 1]); //5
}
