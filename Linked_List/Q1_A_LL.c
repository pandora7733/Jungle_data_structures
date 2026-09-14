//////////////////////////////////////////////////////////////////////////////////

/* CE1007/CZ1007 자료구조
실습 테스트: A 섹션 - 연결 리스트 문제
목적: 문제 1에서 요구하는 함수 구현 */

//////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>

//////////////////////////////////////////////////////////////////////////////////

typedef struct _listnode{
	int item;
	struct _listnode *next;
} ListNode;			// ListNode의 정의를 변경하면 안 됩니다.

typedef struct _linkedlist{
	int size; // 현재 노드의 개수
	ListNode *head; // 첫번째 노드의 주소
} LinkedList;			// LinkedList의 정의를 변경하면 안 됩니다.


///////////////////////// function prototypes ////////////////////////////////////

//이 함수의 함수 원형을 변경하면 안 됩니다.
int insertSortedLL(LinkedList *ll, int item); //연결 리스트에 정수를 삽입합니다. <- 내가 짜야 하는 코드

void printList(LinkedList *ll); //연결 리스트를 출력합니다.
void removeAllItems(LinkedList *ll); //연결 리스트의 모든 노드를 제거합니다.
ListNode *findNode(LinkedList *ll, int index); //연결 리스트에서 특정 인덱스의 노드를 찾습니다.
int insertNode(LinkedList *ll, int index, int value); //연결 리스트에 특정 인덱스에 노드를 삽입합니다.
int removeNode(LinkedList *ll, int index); //연결 리스트에서 특정 인덱스의 노드를 제거합니다.


//////////////////////////// main() //////////////////////////////////////////////

int main()
{
	LinkedList ll;
	int c, i, j;
	c = 1;

	//연결 리스트 1을 빈 연결 리스트로 초기화합니다.
	ll.head = NULL;
	ll.size = 0;

	printf("1: Insert an integer to the sorted linked list:\n"); //연결 리스트에 정수를 삽입합니다.
	printf("2: Print the index of the most recent input value:\n"); //가장 최근에 입력된 값의 인덱스를 출력합니다.
	printf("3: Print sorted linked list:\n"); //정렬된 연결 리스트를 출력합니다.
	printf("0: Quit:"); //종료합니다.

	while (c != 0)
	{
		printf("\nPlease input your choice(1/2/3/0): ");
		scanf("%d", &c);

		switch (c)
		{
		case 1:
			printf("Input an integer that you want to add to the linked list: ");
			scanf("%d", &i);
			j = insertSortedLL(&ll, i);
			printf("The resulting linked list is: ");
			printList(&ll);
			break;
		case 2:
			printf("The value %d was added at index %d\n", i, j);
			break;
		case 3:
			printf("The resulting sorted linked list is: ");
			printList(&ll);
			removeAllItems(&ll);
			break;
		case 0:
			removeAllItems(&ll);
			break;
		default:
			printf("Choice unknown;\n");
			break;
		}


	}
	return 0;
}

//////////////////////////////////////////////////////////////////////////////////

int insertSortedLL(LinkedList *ll, int item)
{

	int index = 0;
	ListNode *cur = ll->head; // ListNode의 주소를 저장

	/* add your code here */
	if (ll->head == NULL) { // 최초 head에 값 넣기
		insertNode(ll, 0, item);
		return index;

	} else { 
		while (cur != NULL) {
			if (cur->item > item) { // 추가 값 위치를 찾아서 값을 넣기
				insertNode(ll, index, item);
				return index;
			}
			index += 1;
			cur = cur->next;
		}
		// 맨 마지막에 값을 새로 추가하기
		insertNode(ll, index, item);
		return index;
	}

}

///////////////////////////////////////////////////////////////////////////////////

void printList(LinkedList *ll){

	ListNode *cur;
	if (ll == NULL)
		return;
	cur = ll->head;

	if (cur == NULL)
		printf("Empty");
	while (cur != NULL)
	{
		printf("%d ", cur->item);
		cur = cur->next;
	}
	printf("\n");
}


void removeAllItems(LinkedList *ll)
{
	ListNode *cur = ll->head;
	ListNode *tmp;

	while (cur != NULL){
		tmp = cur->next;
		free(cur);
		cur = tmp;
	}
	ll->head = NULL;
	ll->size = 0;
}


ListNode *findNode(LinkedList *ll, int index){

	ListNode *temp;

	if (ll == NULL || index < 0 || index >= ll->size)
		return NULL;

	temp = ll->head;

	if (temp == NULL || index < 0)
		return NULL;

	while (index > 0){
		temp = temp->next;
		if (temp == NULL)
			return NULL;
		index--;
	}

	return temp;
}

int insertNode(LinkedList *ll, int index, int value){

	ListNode *pre, *cur;

	if (ll == NULL || index < 0 || index > ll->size + 1)
		return -1;

	// If empty list or inserting first node, need to update head pointer
	if (ll->head == NULL || index == 0){
		cur = ll->head;
		ll->head = malloc(sizeof(ListNode));
		ll->head->item = value;
		ll->head->next = cur;
		ll->size++;
		return 0;
	}


// 	목표 위치의 앞쪽 노드를 찾습니다.
// 	새로운 노드를 생성하고 연결 관계를 다시 연결합니다.
	if ((pre = findNode(ll, index - 1)) != NULL){
		cur = pre->next;
		pre->next = malloc(sizeof(ListNode));
		pre->next->item = value;
		pre->next->next = cur;
		ll->size++;
		return 0;
	}

	return -1;
}


int removeNode(LinkedList *ll, int index){

	ListNode *pre, *cur;

	// 삭제할 수 있는 가장 큰 인덱스는 size - 1입니다.
	if (ll == NULL || index < 0 || index >= ll->size)
		return -1;

	// 첫 번째 노드를 삭제하는 경우 head 포인터를 업데이트해야 합니다.
	if (index == 0){
		cur = ll->head->next;
		free(ll->head);
		ll->head = cur;
		ll->size--;

		return 0;
	}

// 	목표 위치의 앞쪽과 뒤쪽 노드를 찾습니다.
// 	목표 노드의 메모리를 해제하고 연결 관계를 다시 연결합니다.
	if ((pre = findNode(ll, index - 1)) != NULL){

		if (pre->next == NULL)
			return -1;

		cur = pre->next;
		pre->next = cur->next;
		free(cur);
		ll->size--;
		return 0;
	}

	return -1;
}
