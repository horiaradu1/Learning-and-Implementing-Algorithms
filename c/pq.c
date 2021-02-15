#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>

#include "general.h"
#include "graph.h"
#include "pq.h"


/**
 * Implement the interface given in pq.h.
 *
 * We make a few proposals here, but you are welcome to deviate from that, as long as you
 * correctly implement the interface with the specified worst-case complexities!
 *
 */



/**
 * First, we propose a 1-based indexing into the heap, using 0 as "invalid index".
 *
 * Wrapping a heap-index into a structure prevents its accidental confusion with element indexes (Which might save you from a lot of hard-to-find bugs!).
 *
 */

typedef struct {size_t i;} hidx_t;


const hidx_t INVALID_HIDX = {0};
const hidx_t hidx_first = {1};

size_t idx_of(hidx_t i) {return i.i - 1;} /// Convert to zero-based index
bool hidx_is_invalid(hidx_t i) {return i.i == 0;}

// Index operations
hidx_t parent(hidx_t i) {return (hidx_t){i.i / 2}; }
hidx_t left(hidx_t i) {return (hidx_t){i.i * 2}; }
hidx_t right(hidx_t i) {return (hidx_t){i.i * 2 + 1}; }
bool has_parent(hidx_t i) {return parent(i).i>0; }
bool has_left(size_t n, hidx_t i) {return left(i).i<=n; }
bool has_right(size_t n, hidx_t i) {return right(i).i<=n; }

/**
 * The priority queue has 3 main components:
 *   1. An array D that maps nodes to priorities. It is independent from the content of the actual queue.
 *   2. An array H of nodes that encodes the heap of size heap_size.
 *   3. An array I, that maps each node to its current index in H. If a node u is not in the queue, we set H[u] = INVALID_HIDX.
 *
 */
struct _DPQ_t {
    size_t N;     // Number of elements
    size_t heap_size;    // Current size of heap
    weight_t *D;  // Priorities
    node_t *H;    // The heap
    hidx_t *I;    // Index of element in heap.
};


DPQ_t *DPQ_new(size_t N) {
    // Initialize the structure. Allocate enough space for all arrays to hold N elements.
    return NULL;
}

void DPQ_delete(DPQ_t *pq) {
    // Free everything in pq

    // and pq itself
    free(pq);
}

weight_t *DPQ_dist_free(DPQ_t *pq) {
  weight_t *res=pq->D;

  // Free everything but the D-array, which is returned

  // ...

  free(pq);
  return res;
}


weight_t DPQ_prio(DPQ_t const *pq, node_t u) {
  // Its a good idea to use assertions to ensure the preconditions!
  // This makes programs more likely to fail close to the reason of the error, rarher than later, when the (indirect) consequences become apparent.
  assert(u<pq->N);

  return weight_inf(); /// *** return priority of node u
}

/**
 * It is a good idea to wrap repetitive patterns into an own function (though, in C, it can be a pain).
 * This reduces the redundancy, and the chance of accidentally getting one of the repeated versions wrong.
 *
 * In this case, we get the priority associated with a heap index.
 */
weight_t _DPQ_hprio(DPQ_t const *pq, hidx_t i) {
    return DPQ_prio(pq,pq->H[idx_of(i)]);
}


void _DPQ_swap(DPQ_t *pq, hidx_t i, hidx_t j) {
  // Don't forget to update the I array!
}


void _DPQ_sift_up(DPQ_t *pq, hidx_t i) {

}

void _DPQ_sift_down(DPQ_t *pq, hidx_t i) {

  // Don't forget to handle the case that you end up at an index that has a left, but no right child!

}

bool DPQ_contains(DPQ_t const *pq, node_t u) {
    assert(u<pq->N);

    return false; // Use I to check if node is on heap
}


void DPQ_insert(DPQ_t *pq, node_t u, weight_t w) {
  // Insert at end, then sift up

  // Don't forget to update I!
}

bool DPQ_is_empty(DPQ_t const *pq) {return pq->heap_size==0;}

node_t DPQ_pop_min(DPQ_t *pq) {
  assert(pq->heap_size>0);
  // Swap first with last element, decrement heap size, then sift down

  // Don't forget to update I!

  return INVALID_NODE; // Return the node that was removed
}

void DPQ_decrease_key(DPQ_t *pq, node_t u, weight_t w) {
  assert(u<pq->N);
  assert(DPQ_contains(pq,u));
  assert(weight_less(w, pq->D[u]));

  // Update priority, then sift up. Use I to find element's index on the heap
}
