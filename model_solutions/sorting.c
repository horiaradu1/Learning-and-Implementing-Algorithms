
#include <stdlib.h>
#include <stdio.h>
#include "sorting.h"

void sort(struct darray* arr, int select){

  switch(select){
    case BINARY_SEARCH_ONE   : insertion_sort(arr); break;
    case BINARY_SEARCH_TWO   : quick_sort(arr); break;
    case BINARY_SEARCH_THREE :
    case BINARY_SEARCH_FOUR  :
    case BINARY_SEARCH_FIVE  :  // Add your own choices here
    default: 
      fprintf(stderr,
              "The value %d is not supported in sorting.c\n",
              select);
      // Keep this exit code as the tests treat 23 specially
      exit(23);
  }
}


// You may find this helpful
void swap(char* *a, char* *b)
{
        char* temp = *a;
        *a = *b;
        *b = temp;
}



void insertion_sort(struct darray* arr){
        int n = arr->size;
        int i, j;
        char* key;
        // At index i we have sorted the first i elements of the list
        for (i = 1; i < n; i++)
        {
                // Take the next element and insert it into the sorted
                // part of the list in the right place by shifting
                // everything below it up until we can insert it
                key = arr->cells[i];
                j = i-1;
                while (j >= 0 && compare(arr->cells[j],key)>0)
                {
                        arr->cells[j+1] = arr->cells[j];
                        j = j-1;
                }
                arr->cells[j+1] = key;
        }

}


void quick_sort_recursive(struct darray* arr, int start, int end) {
        if (start >= end)
                return;
        // Take the middle element as the pivot 
        char* mid = arr->cells[end];

        // Hoare partition scheme
        // Repeatedly shift find the left and rightmost elements that are on
        // the wrong side and swap them until we meet in the middle
        int left = start, right = end - 1;
        while (left < right) {
                while (compare(arr->cells[left], mid) < 0 && left < right)
                        left++;
                while (compare(arr->cells[right],mid) >= 0 && left < right)
                        right--;
                swap(&arr->cells[left], &arr->cells[right]);
        }
        // Put the pivot in place
        if (compare(arr->cells[left], arr->cells[end]) >=0)
                swap(&arr->cells[left], &arr->cells[end]);
        else
                left++;
        // If the pivot was the smallest element then it's already in sorted
        // position 
        if (left)
                quick_sort_recursive(arr, start, left - 1);
        quick_sort_recursive(arr, left + 1, end);
}
void quick_sort(struct darray* arr) {
        quick_sort_recursive(arr, 0, arr->size - 1);
}

