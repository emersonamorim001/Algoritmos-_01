#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 10000000

//Gerar aleatoriamente um uma Lista de N elementos e ordenar via merge sort, no pior caso O(nlogn)


void Merge(unsigned long long *Lista, unsigned long long *aux, 
           long long esquerda, long long meio, long long direita)
{
    for (long long i = esquerda; i <= direita; i++)
        aux[i] = Lista[i];
    
    long long i = esquerda;
    long long j = meio + 1;
    long long k = esquerda;
    
    while (i <= meio && j <= direita) {
        if (aux[i] <= aux[j])
            Lista[k++] = aux[i++];
        else
            Lista[k++] = aux[j++];
    }
    
    while (i <= meio)
        Lista[k++] = aux[i++];
}

void MergeSort(unsigned long long *Lista, unsigned long long *aux,
               long long esquerda, long long direita)
{
    if (esquerda < direita) {
        long long meio = esquerda + (direita - esquerda) / 2;
        MergeSort(Lista, aux, esquerda, meio);
        MergeSort(Lista, aux, meio + 1, direita);
        Merge(Lista, aux, esquerda, meio, direita);
    }
}

int main() {
    srand((unsigned)time(NULL));
    
    unsigned long long *Lista = (unsigned long long *)malloc(N * sizeof(unsigned long long));
    unsigned long long *aux = (unsigned long long *)malloc(N * sizeof(unsigned long long));
    
    if (Lista == NULL || aux == NULL) {
        printf("Erro ao alocar memória.\n");
        free(Lista);
        free(aux);
        return 1;
    }
    
    for (long long i = 0; i < N; i++) {
        Lista[i] = ((unsigned long long)rand() << 16 | rand()) % N;
    }
    
    clock_t inicio = clock();
    MergeSort(Lista, aux, 0, N - 1);
    clock_t fim = clock();
    
    double tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
    printf("Tempo de execução: %.6f segundos\n", tempo);
    
    free(Lista);
    free(aux);
    return 0;
}