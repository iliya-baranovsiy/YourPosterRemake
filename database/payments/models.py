from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, ForeignKey, Enum, Date, text, BigInteger, String, func, DateTime
from datetime import date, datetime
from .options import PaymentOptions, PLAN_INFO, PaymentStatus
from database.engines import Base


class PaymentModel(Base):
    __tablename__ = "User_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.tg_id'), unique=True)
    payment_plan: Mapped[PaymentOptions] = mapped_column(Enum(PaymentOptions),
                                                         default=PaymentOptions.STANDART,
                                                         server_default=text("'STANDART'"))
    automatic_buy: Mapped[bool] = mapped_column(default=False)
    pending_plan: Mapped[PaymentOptions] = mapped_column(Enum(PaymentOptions),
                                                         default=PaymentOptions.STANDART,
                                                         server_default=text("'STANDART'"))
    priority: Mapped[int] = mapped_column(default=PLAN_INFO[PaymentOptions.STANDART].priority)
    activate_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="payments")

    __table_args__ = (Index("user_payment_index", "user_id", "end_date"),)


class PaymentTransactions(Base):
    __tablename__ = "Payments_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    amount: Mapped[int] = mapped_column(BigInteger)
    telegram_charge_id: Mapped[str] = mapped_column(String, unique=True)
    payload: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (Index("payment_data_index", "user_id", "telegram_charge_id"),)
