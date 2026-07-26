#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 10000000

//Gerar aleatoriamente um uma Lista de N elementos e ordenar via Quick sort, no pior caso O(n²)

void Troca(unsigned long long *a, unsigned long long *b)
{
    unsigned long long temp = *a;
    *a = *b;
    *b = temp;
}

long long Particiona(unsigned long long *Lista, long long baixo, long long alto)
{
    unsigned long long pivo = Lista[alto];
    long long i = baixo - 1;

    for (long long j = baixo; j < alto; j++)
    {
        if (Lista[j] <= pivo)
        {
            i++;
            Troca(&Lista[i], &Lista[j]);
        }
    }

    Troca(&Lista[i + 1], &Lista[alto]);

    return i + 1;
}

void QuickSort(unsigned long long *Lista, long long baixo, long long alto)
{
    if (baixo < alto)
    {
        long long p = Particiona(Lista, baixo, alto);

        QuickSort(Lista, baixo, p - 1);
        QuickSort(Lista, p + 1, alto);
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

	QuickSort(Lista,0,N-1);

	clock_t fim = clock();

	double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;

	printf("Tempo de execução: %.6f segundos\n\n", tempo);

	free(Lista);

	return 0;
}