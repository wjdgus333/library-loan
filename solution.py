# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # 1 이상의 정수만 허용 (True/False는 정수로 보지 않음)
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


def _valid_book(book_id):
    return isinstance(book_id, str) and book_id in BOOKS


class LibraryLoan:
    def __init__(self):
        # book_id -> (name, 빌린 날, 반납 기한)
        self.loans = {}
        # name -> [(정지 시작일, 정지 마지막 날), ...]
        self.suspensions = {}

    def _suspended(self, name, day):
        return any(start <= day <= end for start, end in self.suspensions.get(name, []))

    def borrow(self, book_id, name, day):
        if not _valid_book(book_id) or not _valid_day(day):
            return False
        if book_id in self.loans:
            return False
        mine = [due for (who, _, due) in self.loans.values() if who == name]
        if len(mine) >= MAX_LOANS:
            return False
        if any(day > due for due in mine):
            return False
        if self._suspended(name, day):
            return False
        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_book(book_id) or not _valid_day(day):
            return -1
        loan = self.loans.get(book_id)
        if loan is None or loan[0] != name:
            return -1
        _, borrowed, due = loan
        if day < borrowed:
            return -1
        overdue = max(0, day - due)
        del self.loans[book_id]
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 대출 정지 (겹치면 더 늦게 끝나는 쪽이 적용됨)
            self.suspensions.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        mine = [(book_id, due) for book_id, (who, _, due) in self.loans.items() if who == name]
        return sorted(mine, key=lambda x: (x[1], x[0]))
