/*
 * generic linked-list implementation
 *
 * 2017, Operating Systems
 *
 * DINU Alexandru, 332CB
 *
 */

#ifndef LINKEDLIST_H_
#define LINKEDLIST_H_

#include "utils.h"

typedef struct cell {
	void *data;
	struct cell *next;
} cell_t, *ptr_cell_t;

typedef struct {
	ptr_cell_t cursor;
	ptr_cell_t head, tail;
} clist_t, *ptr_clist_t;



ptr_cell_t new_cell(void *data);

ptr_clist_t clist_init();
void clist_push_back(void *data, ptr_clist_t cl);
void clist_advance_cursor(ptr_clist_t cl);
void clist_move_to_back(ptr_cell_t c, ptr_clist_t cl);
ptr_cell_t clist_find(void *data, size_t sz, ptr_clist_t cl);
void clist_destroy(ptr_clist_t *cl);

int clist_is_empty(ptr_clist_t cl);

#endif
