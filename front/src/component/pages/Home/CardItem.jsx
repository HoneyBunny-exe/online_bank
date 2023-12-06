import React, {useState} from 'react';
import "./CardItem.css";
import {useNavigate} from "react-router-dom";
const CardItem = (props) => {
    const router = useNavigate()
    return (
        <div
            onClick={()=>router(`/cards/${props.card.id}`)}
            className="cardItem">
            <p className="card_type">{props.card.cardType}</p>
            <div className="card_info">
                <img src="/images/card.png" className="cardicon" />
                <p className="num">***{props.card.cardNum}</p>
                <p className="sum">{props.card.balance} ₽</p>
            </div>
        </div>
    );
};

export default CardItem;