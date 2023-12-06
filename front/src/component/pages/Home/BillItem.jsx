import React from 'react';

const BillItem = (props) => {
    return (
        <div className="cardItem">
            <p className="card_type">{props.bill.billType}</p>
            <div className="card_info">
                <p>***{props.bill.billNum}</p>
                <p className="sum">
                    {props.bill.balance} ₽
                </p>
            </div>
        </div>
    );
};

export default BillItem;