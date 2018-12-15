import React, { Component } from 'react';
import axios from "axios";
import './App.css';
import Title from "./components/Title";
import Form from "./components/Form";
import ShowResults from "./components/ShowResults"

class App extends Component {

  /**Holds variables that determine when the page is rerendered */
  state={
    imageUploaded: false,
    imageProcessing: false,
    inspectionResult: "",
    gotImage: false,
    selectedImage: null,
    funFact: "",
  }

  /**Updates state variables [selectedImage], [imageProcessing] after user uploads an image.
  Requires [e]: event object**/
  getPicture = async (e) => {
    let reader = new FileReader()
    const image = e.target.files[0]
    reader.readAsDataURL(image)
    reader.onload = (loaded) => (
    this.setState({selectedImage: loaded.target.result, gotImage: true, 
                    inspectionResult: "", funFact: ""}, function(){
    })
    )
  }

  /** Updates state variables [inspectionResult], [funfact], [imageProcessing] and [error]
  based on result of making a POST request that triggers the neural net and fun fact scraper method. 
  Requires [e]: event object 
  */
  processPicture = async (e) => {   
    e.preventDefault()
    if (this.state.gotImage) { 
      this.setState({imageProcessing: true})
      await axios.post(`http://127.0.0.1:3001/processPic/`, { picbase64: this.state.selectedImage } )
        .then((res) => {
          this.setState({inspectionResult: res.data.result, 
                            funFact: res.data.fun, 
                            imageProcessing: false}, function (){
        })})
        .catch((err)=> {
          this.setState({error: err})
        })           
    }
  }

  /**Runs each time the value of a state variable changes*/
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
                  imageProcessing={this.state.imageProcessing} image={this.state.selectedImage}/>
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
