import React from 'react';
import './CardItem.css'
const CreditCard = (props) => {
    return (
        <div className="cardItem">
            <p className="card_type">{props.credit.creditType}</p>
            <div className="card_info">
                <p>Платеж: {props.credit.datePay}</p>
                <p className="sum">{props.credit.balance} ₽</p>
            </div>
        </div>
    );
};

export default CreditCard;