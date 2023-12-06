import React from 'react';
import {useParams} from "react-router-dom";

const CardHistory = () => {
    const p = useParams()
    return (
        <div>
            HISTORY OF CARD {p.id}
        </div>
    );
};

export default CardHistory;