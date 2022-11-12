#include <stdio.h>
#include <stdlib.h>

//#define N 5 //Numero de nodos de la red
#define INF 10000000// Infinito

//Funcion rellenar matriz: cuenta los ;+1 de la primera fila del .csv
int numero_nodos(char *archivo){
    FILE *f;
    int nodo=1;
    char c;

    f=fopen(archivo,"r");

    if(f==NULL){printf("Error al abrir archivo\n");return 0;}

    //c recorre el fichero y suma 1 por cada ; del .csv
    //nodo=1 y no en 0 porque el último no tiene ;
    while(c!='\n'){
        c=getc(f);
        if(c==';') nodo++;
    }
    fclose(f);

    return nodo;
}

//Función obtener valores iniciales de red: vectores nodo_contiguo y coste_nodo
void valores_iniciales(int *nodo_contiguo,int *coste_nodo,int origen,int num_nod){
    int i;

    //Rellenar nodos
    //Coste del nodo inicialmente será infinito y 0 solo para origen
    //El nodo contiguo, entendido como el accesible a menor coste, no estará definido inicialmente y de ahi el -1

    for(i=0;i<num_nod;i++){
        if(i==origen){
            nodo_contiguo[i]=-1;
            coste_nodo[i]=0;
        }
        else{
            nodo_contiguo[i]=-1;
            coste_nodo[i]=INF;
        }
    }

    return;
}

//Función liberar espacio matriz
void free_matriz_int(int **matriz, int m) {
    int i;

    for (i=0; i<m; i++)
        free(matriz[i]);

    free(matriz);
}

//Funcion reservar memoria lo que ocupa la matriz de red
int** malloc_matriz_int(int m, int n) {
    int i, j, **matriz;

    if ((matriz = (int**) malloc(m*sizeof(int*))) == NULL){
        printf("No fue bien la reserva de memoria");
        return NULL;
        }

    for (i=0; i<m; i++) {
        if ((matriz[i] = (int*) malloc(n*sizeof(int))) == NULL) {
            free_matriz_int(matriz, i);
            return NULL;
        }
    }

    return matriz;
}

//Funcion para coger valores csv y rellenar una matriz que representa la red
void matriz_red(int **red, int N, char *archivo){
    int i=0,j,k=0,l=0;
    FILE *f;
    char c,dato[10];//Restricción: maximo de 10 cifras el dato del csv

    //printf("%s\n",archivo);
    f=fopen(archivo,"r");

    if(f==NULL){printf("Error al abrir archivo\n");return;}

    while(c!=EOF){
        c=getc(f);

        if((c==';')||(c=='\n')||(c==EOF)){
            i=0;//Inicializo el dato
            red[k][l]=strtol(dato,NULL,10);//Convertir string->integer
            l++; //Avanzas una columna, nuevo dato
            //Vaciar la variable dato
            for(j=0;j<10;j++){dato[j]='\0';}
            if(c=='\n'){k++;l=0;}
        }
        else{dato[i]=c;i++;}
    }
    fclose(f);

    return;
}

//Funcion ordenar nodos
void ordenar_nodos(int origen, int *coste_nodo, int *nodo_contiguo,int *nodo_ord,int **M,int N){
    int k=1; //Apunta al siguiente elemento a actualizar. Lo pongo en 1 porque ya incluye el origen
    int j,l,m;
    int nodo_esta; //Comprobar si un nodo esta en nodo_ord

    //El primer nodo debe ser el origen
    nodo_ord[0]=origen;

    //Incluyo nodos conectados al nodo origen
    for(j=0;j<N;j++){
        if(M[origen][j]!=0){
            nodo_ord[k]=j;
            k++;
        }
    }

    //Ahora hay que incluir el resto de nodos
    while(k<N){
        for(l=1;l<k;l++){//El l recorre nodo_ord
            for(j=0;j<N;j++){ //El j recorre cols de M
                if(M[nodo_ord[l]][j]!=0){
                    //Comprobar que el nodo al que apuntamos esta o no incluido
                    nodo_esta=0;
                    for(m=0;m<k;m++){
                        if(j==nodo_ord[m]){nodo_esta=1;}
                    }

                    //Si no lo esta se incluye
                    if(nodo_esta==0){
                        nodo_ord[k]=j;
                        k++;
                    }
                }
                //if(k==N) break; //Salir bucle si ya tenemos todos los nodos
            }
            //if(k==N) break; //Salir bucle si ya tenemos todos los nodos
        }
    }
}

//Actualizar costes nodos
void ajuste_coste_nodos(int *nodo_ord,int *nodo_contiguo,int *coste_nodo,int **M, int N){
    int i,j,coste;

    for(i=0;i<N;i++){ //Recorres vector de nodos
        for(j=0;j<N;j++){ //Fijado nodo, actualizas el resto
            if(M[nodo_ord[i]][j]!=0){ //Se mira si ese nodo j-esimo está conectado con el i-esimo
                coste=coste_nodo[nodo_ord[i]]+M[nodo_ord[i]][j]; //Se obtiene el coste del enlace
                if(coste<coste_nodo[j]){ //Si el coste calculado menor, se actualizan los 2 vectores
                    coste_nodo[j]=coste;
                    nodo_contiguo[j]=nodo_ord[i];
                }
            }
        }
    }
    return;
}

//Sacar camino optimo y su coste
void obtencion_camino(int *nodo_contiguo,int origen,int destino,int N){
    int ruta[N];
    int nodo,i=1;

    //Primero el destino
    ruta[0]=destino;
    nodo=nodo_contiguo[destino];

    while(nodo!=-1){
        ruta[i]=nodo;
        nodo=nodo_contiguo[nodo];
        //printf("%d",i);
        //printf("Ruta= %d\n",ruta[i]);
        i++;
    }
    ruta[i]=origen;

    //Resultado
    int j;
    printf("Ruta=\n");
    for(j=0;j<i;j++){
        printf("%d\n",ruta[j]);
    }

    return;
}


int main(){
    //INPUTS
    int origen,destino;
    printf("Origen = \n");
    scanf("%d",&origen);
    printf("Destino = \n");
    scanf("%d",&destino);

    char archivo_red[8]="red.csv"; //Nombre archivo donde se almacena datos de la red

    //VARIABLES
    int coste; //Coste de la ruta
    int num_nod; //Numero de nodos
    int *nodo_contiguo, *coste_nodo, *nodo_ord;//vectores caracterizan nodos
    int **M; //Matriz de red

    //Obtener el numero de nodos de la red
    num_nod=numero_nodos(archivo_red);
    printf("nodos=\n%d\n",num_nod);

    //Reserva memoria en función del num_nod de la red
    coste_nodo = (int*)malloc(num_nod*sizeof(int));
    nodo_contiguo = (int*)malloc(num_nod*sizeof(int));
    nodo_ord = (int*)malloc(num_nod*sizeof(int));

    if((coste_nodo==NULL)||(nodo_contiguo==NULL)||(nodo_ord==NULL)){
        printf("Reserva memoria para vectores iniciales ha fallado.\n");return 1;}

    if ((M = malloc_matriz_int(num_nod,num_nod)) == NULL) {
        printf("malloc_matriz_int() ha fallado.");
        return 1;
    }

    //Defines la red con la matriz de costes de enlaces y los 2 vectores con coste del nodo y contiguo mas proximo
    valores_iniciales(nodo_contiguo,coste_nodo,origen,num_nod);

    //Rellenas matriz red en base al csv
    matriz_red(M,num_nod,archivo_red);

    //-------------------------------------
    //-----------ALGORITMO DIJKSTRA--------
    //-------------------------------------

     //Los costes de los nodos deben actualizarse en un orden concreto
    ordenar_nodos(origen,coste_nodo,nodo_contiguo,nodo_ord,M,num_nod);

    //Estableciendo un origen, sacas costes de los nodos y el contiguo mas proximo
    ajuste_coste_nodos(nodo_ord,nodo_contiguo,coste_nodo,M,num_nod);

    //Actualizada la info, sacar el camino y su coste
    obtencion_camino(nodo_contiguo,origen,destino,num_nod);

    int i;
    printf("Nodo_contiguo \tNodo_ord\tCoste_nodo\n");
    for (i=0;i<num_nod;i++){
        printf("%d\t%d\t%d\n",nodo_contiguo[i],nodo_ord[i],coste_nodo[i]);
    }

    printf("Coste=\n%d\n",coste_nodo[destino]);


    //Eliminar variables reservadas memoria dinamica
    free_matriz_int(M,num_nod);
    free(nodo_contiguo);
    free(coste_nodo);
    free(nodo_ord);

    return 0;
}

