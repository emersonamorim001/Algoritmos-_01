#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 100000

//Gerar aleatoriamente um uma Lista de N elementos e ordenar via insertion sort, no pior caso O(n²)

void InsertionSort(unsigned long long *Lista)
{
    unsigned long long chave;
    long long j;

    for (size_t i = 1; i < N; i++)
    {
        chave = Lista[i];
        j = i - 1;

        while (j >= 0 && Lista[j] > chave)
        {
            Lista[j + 1] = Lista[j];
            j--;
        }

        Lista[j + 1] = chave;
    }
}

int main()
{
	srand((unsigned)time(NULL));

	unsigned long long *Lista = (unsigned long long *)malloc(N * sizeof(unsigned long long));

	if (Lista == NULL)
	{
		printf("Erro ao alocar memória.\n");
		return 1;
	}

	for (size_t i = 0; i < N; i++)
	{
		Lista[i] = (unsigned long long)rand() % N;
	}

	clock_t inicio = clock();

	InsertionSort(Lista);

	clock_t fim = clock();

	double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;

	printf("Tempo de execução: %.6f segundos\n\n", tempo);

	free(Lista);

	return 0;
}