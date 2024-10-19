from typing import List, Type

from app.utils.exceptions.db import InvalidOrderDirection, OrderColumnNotExist
from app.utils.logging.logger import get_logger

logger = get_logger()


def as_order_by_expression(model: Type["Base"], expression: str) -> List["UnaryExpression"]:  # type: ignore # noqa
    """Convert the ordering expression to the SQLAlchemy UnaryExpression.

    Args:
        model (Base): SQLAlchemy ORM model.

        expression (str): Concatenate column and direction with semi-colon, e.g., 'created_time:desc',
            the direction should only be one of asc and desc.

    Return: sqlalchemy.sql.elements.UnaryExpression
    """
    result = []
    for _express in expression.split(","):
        column, direction = _express.split(":")
        column, direction = column.strip(), direction.strip()
        try:
            db_column = getattr(model, column)
        except AttributeError:
            raise OrderColumnNotExist(column=column)
        try:
            order_function = getattr(db_column, direction)
        except AttributeError:
            raise InvalidOrderDirection(direction=direction)
        result.append(order_function())

    return result
