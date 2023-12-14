import React, {useState} from 'react';
import '../../../styles/Common.css'
import '../../GetItemById/idElements.css'
import './PaymentElem.css'
import Action from "../../../reUse/Action";
import CardList from "../../Home/CardList";
import Window from "../../../reUse/Window";
const Payment = () => {
    return (
        <div className='page_chr'>
            <CardList/>
            <div className="pay_main">
                <div className="pay_btn">
                    <h1 style={{marginLeft:"2%"}}>Переводы</h1>
                    <Action
                        path={'/payment/toOther'}
                        img={'/images/crowd.png'}
                        width={'60'}
                        height={'60'}
                        name={'Другому человеку'}/>
                    <Action
                        path={'/payment/toSelf'}
                        img={'/images/transact.png'}
                        width={'60'}
                        height={'60'}
                        name={'Между своими'}/>
                </div>
                <div className='pay_btn'>
                    <h1 style={{marginLeft:"2%"}}>Платежи</h1>
                    <Action
                        path={'/payment'}
                        img={'/images/plus.png'}
                        width={'60'}
                        height={'60'}
                        name={'Оплатить услугу'}/>
                </div>
            </div>
        </div>
    );
};

export default Payment;