import React from "react";

/** Randomly selects a statement that represents the loading state */
function chooseOne(){
   const loadingSayings = ["hmm...thinking", "tricky one...hmm", 
                                "let me take a closer look...", "loading..."]
   var loading = loadingSayings[Math.floor(Math.random()*loadingSayings.length)]
   return loading
}

/** Dynamic component that gets updated to display result of neural net and fun fact method */
const ShowResults = props => (
    <div>
        <h1 className="results_title"> {props.result} </h1>}
        {props.image == null ?"":<img className="thumbnail"
                                     alt="Your Upload" src={props.image}/>}
        <h3 className="results_sub"> 
        <div className="questionTag">
        {props.result===""?"":"Did you know?\n"}
        </div>
        {props.imageProcessing?chooseOne():props.funFact}
        </h3>
    </div>
);

export default ShowResults;