#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 100000

//Gerar aleatoriamente um uma Lista de N elementos e ordenar via bubble sort, no pior caso O(n²)

void BubbleSort(unsigned long long *Lista)
{
    unsigned long long temp;
    int trocou;

    for (size_t i = 0; i < N - 1; i++)
    {
        trocou = 0;

        for (size_t j = 0; j < N - i - 1; j++)
        {
            if (Lista[j] > Lista[j + 1])
            {
                temp = Lista[j];
                Lista[j] = Lista[j + 1];
                Lista[j + 1] = temp;

                trocou = 1;
            }
        }

        if (trocou == 0)
            break;
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

	BubbleSort(Lista);

	clock_t fim = clock();

	double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;

	printf("Tempo de execução: %.6f segundos\n\n", tempo);

	free(Lista);

	return 0;
}