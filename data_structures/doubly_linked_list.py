class Node:
    """Satu node dalam Doubly Linked List, menyimpan 1 Task."""
    def __init__(self, task):
        self.task = task
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List untuk merepresentasikan timeline tugas.
    Task akan selalu disisipkan terurut berdasarkan deadline (ascending).
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def insert_sorted_by_deadline(self, task):
        """
        Insert task baru ke posisi yang tepat berdasarkan deadline,
        sehingga list selalu terurut dari deadline paling awal -> paling akhir.
        Kompleksitas: O(n) karena harus cari posisi yang tepat.
        """
        new_node = Node(task)

        # Kasus 1: list masih kosong
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
            return

        # Kasus 2: deadline baru lebih awal dari head -> jadi head baru
        if task.deadline < self.head.task.deadline:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            self.size += 1
            return

        # Kasus 3: cari posisi yang tepat (sisipkan setelah node yang sesuai)
        current = self.head
        while current.next is not None and current.next.task.deadline <= task.deadline:
            current = current.next

        new_node.next = current.next
        new_node.prev = current
        if current.next is not None:
            current.next.prev = new_node
        else:
            self.tail = new_node  # disisipkan jadi node terakhir
        current.next = new_node

        self.size += 1

    def remove_by_id(self, task_id):
        """Hapus task tertentu dari list berdasarkan ID. O(n)"""
        current = self.head
        while current is not None:
            if current.task.id == task_id:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # current adalah head

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev  # current adalah tail

                self.size -= 1
                return True
            current = current.next
        return False

    def traverse_forward(self):
        """Mengembalikan list of Task dari awal (deadline tercepat) -> akhir. O(n)"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.task)
            current = current.next
        return result

    def traverse_backward(self):
        """Mengembalikan list of Task dari akhir -> awal. O(n)"""
        result = []
        current = self.tail
        while current is not None:
            result.append(current.task)
            current = current.prev
        return result

    def __len__(self):
        return self.size