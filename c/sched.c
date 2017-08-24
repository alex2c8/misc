#include <stdio.h>
#include <stdlib.h>

#include "clist.h"

#define N 6

ptr_clist_t *clists;


static void invoke_sched(void)
{
	int p, val;

	ptr_clist_t clist;
	ptr_cell_t aux;

	for(p = N - 1; p >= 0; p--) {

		 // there are no threads with current priority p
		if (clist_is_empty(clists[p]))
			continue;

		printf("found non-empty [%d]\n", p);

		clists[p]->cursor = clists[p]->cursor->next;

		 // reset the cursor
		if (clists[p]->cursor == NULL)
			clists[p]->cursor = clists[p]->head;

		 // current_pos -> end
		aux = clists[p]->cursor;
		while (aux != NULL) {
			val = *(int *)(aux->data);
			printf("\t{current_pos -> end}[%d]\n", val);

			// if (val <= 1) {
			// 	printf("[FOUND1]\n");
			// 	return;
			// }

			aux = aux->next;
		}


		 // start -> current_pos
		aux = clists[p]->head;

		while (aux != clists[p]->cursor) {
			val = *(int *)(aux->data);

			printf("\t{start -> current_pos}[%d]\n", val);
			// if (val <= 1) {
			// 	printf("[FOUND2]\n");
			// 	return;
			// }

			aux = aux->next;
		}

	}


	printf("[[[[all done]]]]\n");
}

void print(ptr_clist_t l)
{
	ptr_cell_t aux = l->head;

	while (aux != NULL) {
		printf("[%d] ", *(int*)(aux->data));
		aux = aux->next;
	}
	printf("\n");
}

int main(int argc, char const *argv[])
{
	int cursor, head, tail;

	int *x1 = malloc(sizeof(int));
	int *x2 = malloc(sizeof(int));
	int *x3 = malloc(sizeof(int));
	int *x4 = malloc(sizeof(int));
	int *x5 = malloc(sizeof(int));

	*x1 = 1; *x2 = 2; *x3 = 3; *x4 = 4; *x5 = 5;


	// /* empty */
	// clist = clist_init();

	// clist_push_back(x1, clist);
	// clist_push_back(x2, clist);
	// clist_push_back(x3, clist);
	// clist_push_back(x4, clist);
	// clist_push_back(x5, clist);

	// head = *(int*)(clist->head->data);
	// tail = *(int*)(clist->tail->data);
	// list = *(int*)(clist->list->data);

	// printf("head[%d]\n", head);
	// printf("tail[%d]\n", tail);
	// printf("list[%d]\n", list);

	// printf("\n{moving cursor to the right}\n\n");



	// head = *(int*)(clist->head->data);
	// tail = *(int*)(clist->tail->data);
	// list = *(int*)(clist->list->data);

	// printf("head[%d]\n", head);
	// printf("tail[%d]\n", tail);
	// printf("list[%d]\n", list);

	clists = calloc(N, sizeof(ptr_clist_t));

	int i;
	for (i = 0; i < N; i++) {
		clists[i] = clist_init();
	}

	ptr_clist_t sub_list;

	clist_push_back(x1, clists[0]);
	clist_push_back(x2, clists[0]);
	clist_push_back(x3, clists[0]);
	clist_push_back(x4, clists[0]);
	clist_push_back(x5, clists[0]);

	print(clists[0]);



	clist_move_to_back(clists[0]->tail, clists[0]);

	print(clists[0]);

	ptr_cell_t c = clist_find(x3, sizeof(int), clists[0]);

	printf("[%d]\n", *(int*)(c->next->data));

	//
	// //clist_advance_cursor(clists[0]);
	//
	// head = *(int*)(clists[0]->head->data);
	// tail = *(int*)(clists[0]->tail->data);
	// cursor = *(int*)(clists[0]->cursor->data);
	//
	// printf("head[%d]\n", head);
	// printf("tail[%d]\n", tail);
	// printf("cursor[%d]\n", cursor);



	for (i = 0; i < N; i++)
		clist_destroy(&clists[i]);
	free(clists);



	return 0;
}
