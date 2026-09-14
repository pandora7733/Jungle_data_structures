#!/usr/bin/env python3
"""Generate a Korean translation PDF of Linked Lists Questions."""

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = "/home/sihoo/Projects/Jungle_data_Structures/Linked_List/연결 리스트 문제.pdf"

NAVY = HexColor("#1b365d")
NAVY2 = HexColor("#12263f")
BLUE = HexColor("#0b4f8a")
LINE = HexColor("#d5deea")
BOX = HexColor("#e8eef5")
IO_BG = HexColor("#f3f5f8")
IO_BD = HexColor("#c5ced8")
EX_BG = HexColor("#f8fafc")
EX_BD = HexColor("#d7dee8")
MENU_BG = HexColor("#fff8ee")
MENU_BD = HexColor("#ead9b8")
MUTED = HexColor("#4a5568")
NOTE_BG = HexColor("#eef3f8")
PAGE_W, PAGE_H = A4
LEFT = 16 * mm
RIGHT = 16 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

pdfmetrics.registerFont(TTFont("Malgun", "/usr/share/fonts/wps-fonts/malgun.ttf"))
pdfmetrics.registerFont(TTFont("Malgun-Bold", "/usr/share/fonts/wps-fonts/malgunbd.ttf"))
pdfmetrics.registerFont(TTFont("Consolas", "/usr/share/fonts/wps-fonts/consola.ttf"))
registerFontFamily("Malgun", normal="Malgun", bold="Malgun-Bold")

styles = {
    "kicker": ParagraphStyle(
        "kicker",
        fontName="Malgun-Bold",
        fontSize=8.5,
        leading=12,
        textColor=HexColor("#4a6280"),
        spaceAfter=2,
    ),
    "title": ParagraphStyle(
        "title",
        fontName="Malgun-Bold",
        fontSize=18,
        leading=24,
        textColor=NAVY2,
        spaceAfter=4,
    ),
    "subtitle": ParagraphStyle(
        "subtitle",
        fontName="Malgun",
        fontSize=10.5,
        leading=15,
        textColor=HexColor("#2c3e50"),
        spaceAfter=2,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Malgun",
        fontSize=10,
        leading=15,
        textColor=HexColor("#1a1a1a"),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="Malgun-Bold",
        fontSize=12.4,
        leading=17,
        textColor=NAVY2,
        spaceBefore=4,
        spaceAfter=6,
    ),
    "label": ParagraphStyle(
        "label",
        fontName="Malgun-Bold",
        fontSize=8.2,
        leading=11,
        textColor=NAVY,
        spaceBefore=2,
        spaceAfter=3,
    ),
    "ex": ParagraphStyle(
        "ex",
        fontName="Malgun",
        fontSize=9.6,
        leading=13.8,
        textColor=HexColor("#1a1a1a"),
        alignment=TA_LEFT,
        spaceAfter=2,
    ),
    "menu": ParagraphStyle(
        "menu",
        fontName="Consolas",
        fontSize=8.6,
        leading=12.2,
        textColor=HexColor("#1a1a1a"),
    ),
    "io": ParagraphStyle(
        "io",
        fontName="Consolas",
        fontSize=8.1,
        leading=11.2,
        textColor=HexColor("#1a1a1a"),
    ),
    "proto": ParagraphStyle(
        "proto",
        fontName="Consolas",
        fontSize=9.4,
        leading=13,
        textColor=white,
    ),
    "note": ParagraphStyle(
        "note",
        fontName="Malgun",
        fontSize=9.4,
        leading=13.6,
        textColor=HexColor("#1a1a1a"),
    ),
    "foot": ParagraphStyle(
        "foot",
        fontName="Malgun",
        fontSize=8.4,
        leading=12,
        textColor=MUTED,
    ),
}


def C(s):
    return f'<font name="Consolas" size="9.2" color="#0b4f8a"><b>{s}</b></font>'


def boxed(flowables, bg, bd, pad=7):
    inner = flowables if isinstance(flowables, list) else [flowables]
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.45, bd),
                ("LEFTPADDING", (0, 0), (-1, -1), pad),
                ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 1),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def proto(text):
    t = Table(
        [[Paragraph(text.replace("\n", "<br/>"), styles["proto"])]],
        colWidths=[CONTENT_W],
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY2),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return t


def example(*paras):
    return boxed([Paragraph(x, styles["ex"]) for x in paras], EX_BG, EX_BD)


def menu(text):
    return boxed(Paragraph(text.replace("\n", "<br/>"), styles["menu"]), MENU_BG, MENU_BD)


def io(text):
    rows = []
    empty = []
    for line in text.split("\n"):
        if line:
            shown = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            rows.append([Paragraph(shown, styles["io"])])
        else:
            empty.append(len(rows))
            rows.append([Paragraph("&nbsp;", styles["io"])])
    n = len(rows)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), IO_BG),
        ("BOX", (0, 0), (-1, -1), 0.45, IO_BD),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.4),
        ("TOPPADDING", (0, 0), (0, 0), 6),
        ("BOTTOMPADDING", (0, n - 1), (0, n - 1), 6),
    ]
    for i in empty:
        cmds.append(("TOPPADDING", (0, i), (0, i), 3))
        cmds.append(("BOTTOMPADDING", (0, i), (0, i), 3))
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle(cmds))
    return t


def label(text):
    return Paragraph(text, styles["label"])


def body(text):
    return Paragraph(text, styles["body"])


def h2(text):
    return Paragraph(text, styles["h2"])


def sp(h=4):
    return Spacer(1, h)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 11 * mm, PAGE_W, 11 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Malgun", 8.4)
    canvas.drawString(LEFT, PAGE_H - 7 * mm, "CE1007 / CZ1007 자료구조  ·  섹션 A 연결 리스트 문제 (한국어)")
    canvas.setFont("Malgun-Bold", 8.4)
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 7 * mm, str(doc.page))
    canvas.setFillColor(MUTED)
    canvas.setFont("Malgun", 8)
    canvas.drawCentredString(PAGE_W / 2, 8 * mm, f"- {doc.page} -")
    canvas.restoreState()


Q1_IO = """Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 2
The resulting linked list is: 2

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 3
The resulting linked list is: 2 3

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 5
The resulting linked list is: 2 3 5

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 7
The resulting linked list is: 2 3 5 7

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 9
The resulting linked list is: 2 3 5 7 9

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 8
The resulting linked list is: 2 3 5 7 8 9

Please input your choice(1/2/3/0): 2
The value 8 was added at index 4

Please input your choice(1/2/3/0): 3
The resulting sorted linked list is: 2 3 5 7 8 9

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 5
The resulting linked list is: 2 3 5 7 8 9

Please input your choice(1/2/3/0): 2
The value 5 was added at index -1

Please input your choice(1/2/3/0): 3
The resulting sorted linked list is: 2 3 5 7 8 9

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 11
The resulting linked list is: 2 3 5 7 8 9 11

Please input your choice(1/2/3/0): 2
The value 11 was added at index 6

Please input your choice(1/2/3/0): 3
The resulting sorted linked list is: 2 3 5 7 8 9 11"""

Q5_IO = """Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 2
The resulting linked list is: 2

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 3
The resulting linked list is: 2 3

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 5
The resulting linked list is: 2 3 5

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 6
The resulting linked list is: 2 3 5 6

Please input your choice(1/2/3/0): 1
Input an integer that you want to add to the linked list: 7
The resulting linked list is: 2 3 5 6 7

Please input your choice(1/2/3/0): 2
The resulting linked list is: 2 3 5 6 7

Please input your choice(1/2/3/0): 3
The resulting linked lists after splitting the given linked list are:
Front linked list: 2 3 5
Back linked list: 6 7"""

Q6_IO = """Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 30
The Linked List is: 30

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 20
The Linked List is: 30 20

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 40
The Linked List is: 30 20 40

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 70
The Linked List is: 30 20 40 70

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 50
The Linked List is: 30 20 40 70 50

Please input your choice(1/2/0): 2
The resulting Linked List is: 70 30 20 40 50

Please input your choice(1/2/0): 0"""

Q7_IO = """Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 1
The resulting Linked List is: 1

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 2
The resulting Linked List is: 1 2

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 3
The resulting Linked List is: 1 2 3

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 4
The resulting Linked List is: 1 2 3 4

Please input your choice(1/2/0): 1
Input an integer that you want to add to the linked list: 5
The resulting Linked List is: 1 2 3 4 5

Please input your choice(1/2/0): 2
The resulting Linked List after reversing its elements is: 5 4 3 2 1

Please input your choice(1/2/0): 0"""


def build():
    story = []

    story.append(Paragraph("CE1007 / CZ1007 자료구조 · 실습 테스트", styles["kicker"]))
    story.append(Paragraph("섹션 A – 연결 리스트", styles["title"]))
    story.append(
        Paragraph(
            "이 섹션에서 지정된 문제 1개를 풀어 답하시오.<br/>"
            "[Answer 1 Specified Question from this Section]",
            styles["subtitle"],
        )
    )
    story.append(sp(8))
    story.append(
        boxed(
            Paragraph(
                "<b>안내:</b> 각 문제의 프로그램 템플릿은 APAS 시스템에 제공됩니다. "
                "반드시 해당 템플릿을 사용하여 함수를 구현해야 합니다. "
                "아래 입출력 예시의 문구는 원본(영어)과 동일합니다. 실제 프로그램 출력도 영어입니다.",
                styles["note"],
            ),
            NOTE_BG,
            NAVY,
            pad=8,
        )
    )
    story.append(sp(10))

    # Q1
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"1. ({C('insertSortedLL')})"),
                body(
                    f"C 함수 {C('insertSortedLL()')}을 작성하시오. 이 함수는 사용자에게 정수를 입력받은 뒤, "
                    "그 값을 연결 리스트에 <b>오름차순</b>으로 삽입합니다."
                ),
                body(
                    "이미 현재 연결 리스트에 존재하는 정수는 삽입하지 않습니다. "
                    "함수는 새 항목이 추가된 <b>인덱스 위치</b>를 반환해야 합니다. "
                    f"삽입에 실패하면 {C('-1')}을 반환합니다. "
                    "연결 리스트는 이미 정렬된 리스트이거나 빈 리스트라고 가정합니다."
                ),
                label("함수 원형"),
                proto("int insertSortedLL(LinkedList *ll, int item);"),
            ]
        )
    )
    story.append(sp(7))
    story.append(
        example(
            f"현재 연결 리스트가 <b>2, 3, 5, 7, 9</b>일 때, 값 <b>8</b>로 {C('insertSortedLL()')}을 호출하면 결과는 다음과 같습니다.",
            "<b>2, 3, 5, 7, 8, 9</b>",
            "새 항목이 추가된 인덱스: <font name='Consolas' size='8.6'>The value 8 was added at index 4</font>",
        )
    )
    story.append(sp(5))
    story.append(
        example(
            "현재 연결 리스트가 <b>5, 7, 9, 11, 15</b>일 때, 값 <b>7</b>로 호출하면 리스트는 그대로입니다.",
            "<b>5, 7, 9, 11, 15</b>",
            f"7은 이미 있으므로 삽입에 실패하고 {C('-1')}을 반환합니다.",
            "<font name='Consolas' size='8.6'>The value 7 was added at index -1</font>",
        )
    )
    story.append(sp(6))
    story.append(label("메뉴"))
    story.append(
        menu(
            "1: Insert an integer to the sorted linked list:\n"
            "2: Print the index of the most recent input value:\n"
            "3: Print sorted linked list:\n"
            "0: Quit:"
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(io(Q1_IO))

    # Q2
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"2. ({C('alternateMergeLL')})"),
                body(
                    f"C 함수 {C('alternateMergeLL()')}을 작성하시오. 이 함수는 <b>두 번째 리스트의 노드</b>를 "
                    "<b>첫 번째 리스트의 교차 위치</b>(한 칸씩 번갈아 넣는 자리)에 삽입합니다. "
                    "두 번째 리스트의 노드는 첫 번째 리스트에 교차 삽입할 위치가 남아 있을 때만 삽입합니다."
                ),
                label("함수 원형"),
                proto("void alternateMergeLL(LinkedList *ll1, LinkedList *ll2);"),
            ]
        )
    )
    story.append(sp(7))
    story.append(
        example(
            "두 연결 리스트가 다음과 같다고 가정합니다.",
            "LinkedList1: <b>1, 2, 3</b>",
            "LinkedList2: <b>4, 5, 6, 7</b>",
            "결과는 다음과 같습니다.",
            "LinkedList1: <b>1, 4, 2, 5, 3, 6</b>",
            "LinkedList2: <b>7</b>",
        )
    )
    story.append(sp(5))
    story.append(
        example(
            "첫 번째 리스트가 두 번째 리스트보다 길면, 두 번째 리스트는 비게 됩니다.",
            "LinkedList1: <b>1, 5, 7, 3, 9, 11</b>",
            "LinkedList2: <b>6, 10, 2, 4</b>",
            "결과는 다음과 같습니다.",
            "LinkedList1: <b>1, 6, 5, 10, 7, 2, 3, 4, 9, 11</b>",
            "LinkedList2: <b>empty</b>",
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(
        body(
            "현재 리스트가 Linked list 1: 1, 2, 3 이고 Linked list 2: 4, 5, 6, 7 인 경우:"
        )
    )
    story.append(
        io(
            "Linked list 1: 1 2 3\n"
            "Linked list 2: 4 5 6 7\n"
            "\n"
            "Please input your choice(1/2/3/0): 3\n"
            "The resulting linked lists after merging the given linked list are:\n"
            "Linked list 1: 1 4 2 5 3 6\n"
            "Linked list 2: 7"
        )
    )

    # Q3
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"3. ({C('moveOddItemsToBackLL')})"),
                body(
                    f"C 함수 {C('moveOddItemsToBackLL()')}을 작성하시오. "
                    "이 함수는 연결 리스트의 <b>모든 홀수 정수</b>를 리스트의 <b>뒤쪽</b>으로 이동시킵니다."
                ),
                label("함수 원형"),
                proto("void moveOddItemsToBackLL(LinkedList *ll);"),
            ]
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(
        example(
            "연결 리스트가 <b>2, 3, 4, 7, 15, 18</b>이면:",
            "The resulting Linked List after moving odd integers to the back of the Linked List is: <b>2 4 18 3 7 15</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>2, 7, 18, 3, 4, 15</b>이면:",
            "The resulting Linked List after moving odd integers to the back of the Linked List is: <b>2 18 4 7 3 15</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>1, 3, 5</b>이면:",
            "The resulting Linked List after moving odd integers to the back of the Linked List is: <b>1 3 5</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>2 4 6</b>이면:",
            "The resulting Linked List after moving odd integers to the back of the Linked List is: <b>2 4 6</b>",
        )
    )

    # Q4
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"4. ({C('moveEvenItemsToBackLL')})"),
                body(
                    f"C 함수 {C('moveEvenItemsToBackLL()')}을 작성하시오. "
                    "이 함수는 연결 리스트의 <b>모든 짝수 정수</b>를 리스트의 <b>뒤쪽</b>으로 이동시킵니다."
                ),
                label("함수 원형"),
                proto("void moveEvenItemsToBackLL(LinkedList *ll);"),
            ]
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(
        example(
            "연결 리스트가 <b>2, 3, 4, 7, 15, 18</b>이면:",
            "The resulting Linked List after moving even integers to the back of the Linked List is: <b>3 7 15 2 4 18</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>2, 7, 18, 3, 4, 15</b>이면:",
            "The resulting Linked List after moving even integers to the back of the Linked List is: <b>7 3 15 2 18 4</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>1, 3, 5</b>이면:",
            "The resulting Linked List after moving even integers to the back of the Linked List is: <b>1 3 5</b>",
        )
    )
    story.append(sp(4))
    story.append(
        example(
            "연결 리스트가 <b>2 4 6</b>이면:",
            "The resulting Linked List after moving even integers to the back of the Linked List is: <b>2 4 6</b>",
        )
    )

    # Q5
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"5. ({C('frontBackSplitLL')})"),
                body(
                    f"C 함수 {C('frontBackSplitLL()')}을 작성하시오. 이 함수는 단일 연결 리스트를 두 개의 부분 리스트로 나눕니다. "
                    "하나는 <b>앞쪽 절반(front half)</b>, 다른 하나는 <b>뒤쪽 절반(back half)</b>입니다. "
                    "원소 개수가 <b>홀수</b>이면 남는 원소는 <b>앞쪽 리스트</b>에 넣습니다. "
                    f"{C('frontBackSplitLL()')}은 {C('frontList')}와 {C('backList')} 두 리스트를 출력합니다."
                ),
                label("함수 원형"),
                proto(
                    "void frontBackSplitLL(LinkedList *ll,<br/>"
                    "&nbsp;&nbsp;&nbsp;&nbsp;LinkedList *resultFrontList,<br/>"
                    "&nbsp;&nbsp;&nbsp;&nbsp;LinkedList *resultBackList);"
                ),
            ]
        )
    )
    story.append(sp(7))
    story.append(
        example(
            "주어진 연결 리스트가 <b>2, 3, 5, 6, 7</b>이면, 결과는 다음과 같습니다.",
            "frontList: <b>2, 3, 5</b>",
            "backList: <b>6, 7</b>",
        )
    )
    story.append(sp(6))
    story.append(label("메뉴"))
    story.append(
        menu(
            "1: Insert an integer to the linked list:\n"
            "2: Print the linked list:\n"
            "3: Split the linked list into two linked lists, frontList and backList:\n"
            "0: Quit:"
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(io(Q5_IO))

    # Q6
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"6. ({C('moveMaxToFront')})"),
                body(
                    f"C 함수 {C('moveMaxToFront()')}를 작성하시오. 이 함수는 정수를 담은 연결 리스트를 "
                    "<b>최대 한 번만</b> 순회한 뒤, <b>가장 큰 값을 저장한 노드</b>를 리스트의 <b>맨 앞</b>으로 이동시킵니다."
                ),
                label("함수 원형"),
                proto("int moveMaxToFront(ListNode **ptrHead);"),
            ]
        )
    )
    story.append(sp(7))
    story.append(
        example(
            "연결 리스트가 <b>(30, 20, 40, 70, 50)</b>이면, 결과는 <b>(70, 30, 20, 40, 50)</b>입니다."
        )
    )
    story.append(sp(6))
    story.append(label("메뉴"))
    story.append(
        menu(
            "1: Insert an integer to the linked list:\n"
            "2: Move the node with the largest stored value to the front of the list:\n"
            "0: Quit:"
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(io(Q6_IO))

    # Q7
    story.append(sp(12))
    story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=8))
    story.append(
        KeepTogether(
            [
                h2(f"7. ({C('recursiveReverse')})"),
                body(
                    f"C 함수 {C('recursiveReverse()')}를 작성하시오. 이 함수는 <b>재귀</b>를 사용하여 "
                    f"{C('next')} 포인터와 {C('head')} 포인터를 바꿔, 주어진 연결 리스트를 뒤집습니다."
                ),
                label("함수 원형"),
                proto("void recursiveReverse(ListNode **ptrHead);"),
            ]
        )
    )
    story.append(sp(7))
    story.append(
        example(
            "연결 리스트가 <b>(1, 2, 3, 4, 5)</b>이면, 결과는 <b>(5, 4, 3, 2, 1)</b>입니다."
        )
    )
    story.append(sp(6))
    story.append(label("메뉴"))
    story.append(
        menu(
            "1: Insert an integer to the linked list:\n"
            "2: Reversed Linked List:\n"
            "0: Quit:"
        )
    )
    story.append(sp(6))
    story.append(label("입출력 예시"))
    story.append(io(Q7_IO))

    story.append(sp(14))
    story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=6))
    story.append(
        Paragraph(
            "원본: Linked Lists Questions.pdf · 한국어 번역본 · "
            "원본 PDF에 있던 손글씨 메모는 포함하지 않았습니다.",
            styles["foot"],
        )
    )
    return story


def main():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        title="섹션 A – 연결 리스트 문제",
        author="한국어 번역",
    )
    doc.build(build(), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    main()
