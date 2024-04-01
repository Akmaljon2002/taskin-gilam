from typing import Optional
from datetime import datetime
from random import choices
import string


def generate_random_string(length: int) -> str:
    return ''.join(choices(string.ascii_letters + string.digits, k=length))


async def reform_text(
        text_str: str,
        user: Optional[str] = None,
        summa: Optional[str] = None,
        hajm: Optional[str] = None,
        order_id: Optional[str] = None,
        xizmat_turi: Optional[str] = None,
        total_price: Optional[str] = None,
        maxsulot_detalni: Optional[str] = None,
        operator: Optional[str] = None,
        operator_phone: Optional[str] = None,
        transport_phone: Optional[str] = None,
        transport: Optional[str] = None
):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rstring = generate_random_string(256)

    replacements = {
        "{date}": current_date,
        "{rstring}": rstring,
        "{user}": user,
        "{summa}": summa,
        "{hajm}": hajm,
        "{order_id}": order_id,
        "{xizmat_turi}": xizmat_turi,
        "{total_price}": total_price,
        "{maxsulot_detalni}": maxsulot_detalni,
        "{operator}": operator,
        "{operator_phone}": operator_phone,
        "{transport_phone}": transport_phone,
        "{transport}": transport
    }

    for key, value in replacements.items():
        if key in text_str:
            if value:
                text_str = text_str.replace(key, str(value))

    return text_str

