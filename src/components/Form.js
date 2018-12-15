import React from "react";

/** Dynamic component that responds to clicking to get an image and clicking to process it*/
const Form = props => (
	<form >
        <label className="custom-file-upload">
        <input type="file" accept="image/*" onChange={props.getPicture}/>
                Get Picture
        </label>
        <button onClick={props.processPicture}>Process</button>
	</form>
);

export default Form;


