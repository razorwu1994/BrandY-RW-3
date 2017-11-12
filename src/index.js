import React from 'react';
import ReactDOM from 'react-dom';
import {Button} from 'react-bootstrap';
import './index.css';
import {randCoordinates,gen_everything,sfCells,pathConfig,gen_start_final_cells} from './constants.js'
import FileReaderInput from 'react-file-reader-input';
import ReactFileReader from 'react-file-reader'

const BLOCKED_CELL = 0
const REG_UNBLOCKED_CELL = 1
const HARD_TRAVERSE_CELL = 2
const REG_UNBLOCKED_HWY_CELL = 'a'
const HARD_TRAVERSE_HWY_CELL = 'b'
const row = 120,col=160
gen_everything();
var fileConfig = []

  class Board extends React.PureComponent  {
    constructor(props) {
        super(props);
        this.state = {
            dataMatrix:Array(120).fill(Array(160).fill(0)),
            genSFtoggle:false,            
        };
    }
    renderSquare(r,c,handleClick,cellType) {
      const colorGroup={'-1':'blue',0:'lightcoral',1:'white',2:'lightgrey','a':'white','b':'lightgrey'}
      const labelGroup={s:'S',f:'G'}
      return (
          <Button key={r+","+c} value={r+","+c+",gvalue-"+1} className="square" cursor="pointer" onClick={handleClick}
          style={{background:colorGroup[cellType]}}>
          {cellType==='a'&&<span class="separator"></span>}
          {cellType==='b'&&<span class="separator"></span>}
          {this.props.inputToggle===false&&sfCells[0]===r+","+c&&<span style={{width:'100%',color:'blue',fontSize:'1.5vmin'}}>S</span>}
          {this.props.inputToggle===false&&sfCells[1]===r+","+c&&<span style={{width:'100%',color:'blue',fontSize:'1.5vmin'}}>G</span>}
          </Button>
      );
    }

    genNewSF=()=>{
      this.setState({genSFtoggle:!this.state.genSFtoggle})
      gen_start_final_cells()      
    }

    handleClick= (e)=>{
        let location = e.target.value,
            updateInfo = "The clicked cell is "+location
        console.log(updateInfo)
    }

    outputFile = ()=>{
      //sfCells,randCoordinates,hardTraverseCoordinates
      var config=[pathConfig,fileConfig]
      var index=0

      var partStr1 = sfCells[0]+"\n"+sfCells[1]+"\n"
      for(let temp in randCoordinates){
        if(temp === 7) {
          partStr1+=randCoordinates[temp]
        }
        else partStr1+=randCoordinates[temp]+"\n"
      }
      var partStr2
      if(this.props.inputToggle){
        index=1
      }
        partStr2 = config[index].reduce((a,b)=>{
        if(a.length===0){
            let temp=""
            for(let c =0;c<b.length;c++)
                temp+=b[c]
            return temp
        }
        else{
          let atemp=""
          for(let c =0;c<a.length;c++)
              atemp+=a[c]
          let btemp=""
          for(let c =0;c<b.length;c++)
                  btemp+=b[c]
          return atemp+"\n"+btemp
        }
      },""
      )
      //console.log(partStr2)
      //console.log(pathConfig)
      //
      if(this.props.outputToggle){
        var FileSaver = require('file-saver');
        var blob = new Blob([partStr1.trim()+"\n"+partStr2], {type: "text/plain;charset=utf-8"});
        FileSaver.saveAs(blob, "mapconfig.txt");

      }
      this.props.closeOutput
    }

    render() {
        let r,c
        var board =[]
        var rows =[]
        let cellType = REG_UNBLOCKED_CELL
        if(this.props.inputToggle){
          var tmp = this.props.fileConfig.split("\n").slice(10)
          fileConfig=[]
          for(let r=0;r<120;r++){
            fileConfig.push([])
            for(let c=0;c<160;c++){
              fileConfig[r].push(tmp[r].charAt(c))
            }
          }

        }
        for(r=0;r<row;r++){
            for(c=0;c<col;c++){
              if(!this.props.inputToggle){
                    cellType=pathConfig[r][c]

                      //blue color center
                      // for(let cc in randCoordinates)
                      //   if(r===randCoordinates[cc][0]&&c===randCoordinates[cc][1])
                      //           cellType=-1
              }
              else{//take an input file
                  cellType=fileConfig[r][c]
              }
             rows.push(this.renderSquare(r,c,this.handleClick,cellType))
            }
            board.push(
                <div className="board">
                    {rows}
                </div>
            )
            rows=[]
        }
        this.outputFile()
        return (
        <div style={{overflowX:'visible',overflowY:'visible',width:'200%',height:'150%'}}>
        <Button onClick={this.genNewSF}>gen new start and goal</Button>
        {board}
        </div>
      );
    }
  }

  class Game extends React.Component {
    constructor(){
      super()
      this.state={
        inputToggle:false,
        outputToggle:false,
        config:"",
      }
    }

    uploadFile=(result)=>{
      this.setState({config:result})
    }
    handleChange = (files) => {
        if(files[0]  === null){
          this.setState({inputToggle:false})
          console.log("NULL file")
          return
        }
        var reader = new FileReader();
        reader.onload = (e) =>{
        // Use reader.result
        this.uploadFile(reader.result)
        }
        reader.readAsText(files[0]);
           setTimeout(()=>{
                    this.setState({inputToggle:true})
            }, 1000);
    }

    closeOutput=()=>{
      this.setState({outputToggle:false})
    }  


    render() {
      return (
        <div>
        <div style={{display:'flex'}}>
          <Button>Uniform Cost</Button>
          <Button onClick={(e)=>this.setState({outputToggle:!this.state.outputToggle})}>File Output</Button>
          <div style={{width:'90px'}}>
          <ReactFileReader handleFiles={this.handleChange} fileTypes={'.txt'} >
              <Button cursor="pointer" style={{width:"100%"}}>Upload</Button>
          </ReactFileReader>
          </div>
        </div>
        <Board
        closeOutput={this.closeOutput}
        fileConfig={this.state.config}
        inputToggle={this.state.inputToggle}
        outputToggle={this.state.outputToggle}
        />
        </div>

      );
    }
  }

  // ========================================

  ReactDOM.render(<Game />, document.getElementById("root"));
