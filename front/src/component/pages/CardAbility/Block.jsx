import React from 'react';
import {useParams} from "react-router-dom";

const Block = () => {
   const p = useParams()
    return (
        <div>
            block card with id {p.id}
        </div>
    );
};

export default Block;