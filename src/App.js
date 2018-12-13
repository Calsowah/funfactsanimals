// to run :
//     1. npm install
//     2. npm start
import React, { Component } from 'react';
import axios from "axios";
import Cropper from "react-cropper";
import './App.css';
import Title from "./components/Title";
import Form from "./components/Form";
import ShowResults from "./components/ShowResults"

class App extends Component {
  state={
    imageUploaded: false,
    imageProcessing: false,
    inspectionResult: "Kendrick Lamar",
    selectedImage: null,
    funFact: "I am the one"
  }

  getPicture = async (e) => {
    let reader = new FileReader()
    const image = e.target.files[0]
    reader.readAsDataURL(image)
    console.log("sddsds")
    reader.onload = (e) => (
    this.setState({selectedImage: e.target.result, imageProcessing: true}, function(){
      console.log(this.state.imageProcessing)
    })
    )
}

  //places a get request that should return an object containing result of neural net and fun fact
  processPicture = async (e) => {   
   if (this.state.imageProcessing) { 
    await axios.get(`http://127.0.0.1:5000/processPic/${this.state.selectedImage}`)
   .then((res) => {
              this.setState({inspectionResult: res}, function (){console.log("yay")})})
    .catch((e)=> {
      console.log("Oops")
    })           
}}

  render() {
    return (
      <div>
        <div className="wrapper">
          <div className="main">
            <div className="container">
              <div className="row">
                <div className="col-xs-5 title-container">
                  <Title />
                </div>
                <div className="col-xs-7 form-container">
                  <Form getPicture={this.getPicture} processPicture={this.processPicture} />

                  <ShowResults result={this.state.inspectionResult} funFact={this.state.funFact}
                   image={this.state.selectedImage}/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
