import React from "react";

const ShowResults = props => (
    <div>
   
        <h1 className="results_title"> {props.result} </h1>
         {props.image == null ?<text>""</text>:<img className="thumbnail" src={props.image}/>}
        <h3 className="results_sub"> {props.funFact}</h3>
    </div>
);

export default ShowResults;