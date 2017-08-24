/*
 * generic linked-list implementation
 *
 * 2017, Operating Systems
 *
 * DINU Alexandru, 332CB
 *
 */

#include "clist.h"


ptr_clist_t clist_init()
{
	ptr_clist_t cl = calloc(1, sizeof(clist_t));

	cl->cursor = NULL;
	cl->head = NULL;
	cl->tail = NULL;

	return cl;
}

/* add a new cell with ref to data  */
ptr_cell_t new_cell(void *data)
{
	ptr_cell_t aux;

	aux = calloc(1, sizeof(cell_t));
	DIE(aux == NULL, "calloc");

	aux->data = data;
	aux->next = NULL;

	return aux;
}


void clist_push_back(void *data, ptr_clist_t cl)
{
	ptr_cell_t aux = new_cell(data);

	if (cl->cursor == NULL) {
		cl->cursor = aux;
		cl->head = aux;
		cl->tail = aux;
	} else {
		cl->tail->next = aux;
		cl->tail = aux;
	}

}

void clist_advance_cursor(ptr_clist_t cl)
{
	cl->cursor = cl->cursor->next;

	if (cl->cursor == NULL)
		cl->cursor = cl->head;
}

void clist_move_to_back(ptr_cell_t c, ptr_clist_t cl)
{
	ptr_cell_t aux, before;

	if (c == cl->tail)
		return;

	before = NULL;
	aux = cl->head;

	while (aux != c) {
		before = aux;
		aux = aux->next;
	}

	if (before == NULL) {
		aux = cl->head;
		cl->head = cl->head->next;


	} else {
		before->next = c->next;
	}

	cl->tail->next = c;
	cl->tail = c;
	cl->tail->next = NULL;
}

ptr_cell_t clist_find(void *data, size_t sz, ptr_clist_t cl)
{
	ptr_cell_t aux;

	for (aux = cl->head; aux != NULL; aux = aux->next) {
		if (memcmp(aux->data, data, sz) == 0)
			return aux;
	}

	return NULL;
}


void clist_destroy(ptr_clist_t *cl)
{
	ptr_cell_t cursor, aux;

	if (*cl == NULL)
		return;

	cursor = (*cl)->head;

	while(cursor != NULL) {
		aux = cursor;
		cursor = cursor->next;

		free(aux->data);
		aux->data = NULL;

		free(aux);
		aux = NULL;
	}

	free(*cl);
	*cl = NULL;
}

int clist_is_empty(ptr_clist_t cl)
{
	int x = 1;

	x &= (cl->cursor == NULL);
	x &= (cl->head == NULL);
	x &= (cl->tail == NULL);

	return x;
}
