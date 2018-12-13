import React from "react";

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


