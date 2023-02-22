#include <stdio.h>

void quick_sort(int[], int, int);
int partition(int[], int, int);

#define MAX_SIZE 50

// The program reads <= MAX_SIZE integer elements from stdin, sorts them using qsort, and outputs sorted array.
int main()
{
  int n = 0;
  int val;
  int a[MAX_SIZE];
  while (scanf("%d", &val) > 0)
  {
    if (n < MAX_SIZE)
    {
      a[n] = val;
      ++n;
    }
    else
    {
      fprintf(stderr, "Error: too many elements given\n");
      return 1;
    }
  }

  if (n == 0)
  {
    fprintf(stderr, "Error: there are no elements given\n");
    return 1;
  }

  quick_sort(a, 0, n - 1);

  for (int i = 0; i < n; i++)
  {
    printf("%d ", a[i]);
  }
  printf("\n");
  return 0;
}

// Quick sort Algorithm

void quick_sort(int a[], int l, int u)
{
  if (l < u)
  {
    int j = partition(a, l, u);
    quick_sort(a, l, j - 1);
    quick_sort(a, j + 1, u);
  }
}

int partition(int a[], int l, int u)
{
  int v, i, j, temp;
  v = a[l];
  i = l;
  j = u + 1;

  do
  {
    do
    {
      i++;
    } while (a[i] < v && i <= u);

    do
    {
      j--;
    } while (v < a[j]);

    if (i < j)
    {
      temp = a[i];
      a[i] = a[j];
      a[j] = temp;
    }
  } while (i < j);

  a[l] = a[j];
  a[j] = v;

  return (j);
}
