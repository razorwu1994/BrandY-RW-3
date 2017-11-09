const row = 120,col=160
export var randCoordinates =[]
export var highWayCoordinates =[]
var getRandomInt = function (min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}
var gen_hard_cells=()=>{
    let counter=0;
    while(counter<8){
        randCoordinates.push([""])
        let xCor = getRandomInt(0,row)
        let yCor = getRandomInt(0,col)
        randCoordinates[counter][0]=xCor
        randCoordinates[counter][1]=yCor
        counter++
    }
}


var gen_hwy_cells=()=>{
    let xCor = getRandomInt(0,row)
    let yCor = getRandomInt(0,col)
    var startingCell
        ,nextDirection; 
    var rand = Math.random()
    if(rand<=0.25){
        startingCell=[xCor,0]        
        nextDirection=1// 1 : next move Down
    }
    else if(rand<=0.5){
        startingCell=[0,yCor]
        nextDirection=2// 2 : next move Right
    }
    else if(rand<=0.75){
        startingCell=[row-1,yCor]
        nextDirection=3// 3 : next move Left
    }
    else{
        startingCell=[xCor,col-1]        
        nextDirection=4// 4:  next move Up
    }
    
    var currentCell=startingCell
    highWayCoordinates.push(parseInt(currentCell[0])+","+parseInt(currentCell[1]))
    var prevDirection = nextDirection
    do{
        rand = Math.random()        
        switch (nextDirection){
            case 1://prev Down
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[0]))+","+(parseInt(currentCell[1])+parseInt(i+1)))
                        !==-1){
                            nextDirection = prevDirection
                            break;                            
                        }
                    }                
                    if(parseInt(currentCell[1])+20> col-1){
                        if (col-1-parseInt(currentCell[1])+highWayCoordinates.length>=100){
                        for(let i=0;i<col-1-parseInt(currentCell[1]);i++){
                            highWayCoordinates.push((parseInt(currentCell[0]))+","+(parseInt(currentCell[1])+parseInt(i+1)))                            
                            }
                            return;                                                        
                        }
                        nextDirection = prevDirection
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[0]))+","+(parseInt(currentCell[1])+parseInt(i+1)))
                    }
                    currentCell[1]=parseInt(currentCell[1])+20
                    if(rand<=0.2)//20% go Right
                    {
                        prevDirection = nextDirection                        
                        nextDirection = 2
                    }
                    else if(rand<=0.4){//20% go Left
                        prevDirection = nextDirection                                                
                        nextDirection = 3 
                    } 
                    //60% same direction
                    break;
            case 2://Right
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[0])+parseInt(i+1))+","+parseInt(currentCell[1]))
                        !==-1){
                            nextDirection = prevDirection
                            break;                            
                        }
                    } 
                    if(parseInt(currentCell[0])+20> col-1){
                        if (col-1-parseInt(currentCell[0])+highWayCoordinates.length>=100){
                        for(let i=0;i<col-1-parseInt(currentCell[0]);i++){
                            highWayCoordinates.push((parseInt(currentCell[0])+parseInt(i+1))+","+parseInt(currentCell[1]))                            
                            }
                            return;                                                        
                        }
                        nextDirection = prevDirection
                        break;                        
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[0])+parseInt(i+1))+","+parseInt(currentCell[1]))
                    }
                    currentCell[0]=parseInt(currentCell[0])+20
                    if(rand<=0.2)//20% go Down
                    {
                        prevDirection = nextDirection                        
                        nextDirection = 1
                    }
                    else if(rand<=0.4){//20% go Up
                        prevDirection = nextDirection                                                
                        nextDirection = 4 
                    } 
                    //60% same direction
                    break;
            case 3://Left
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[0])-parseInt(i+1))+","+parseInt(currentCell[1]))
                        !==-1){
                            nextDirection = prevDirection
                            break;                            
                        }
                    } 
                    if(parseInt(currentCell[0])-20<0){
                        if (parseInt(currentCell[0])+highWayCoordinates.length>=100){
                        for(let i=0;i<parseInt(currentCell[0]);i++){
                            highWayCoordinates.push((parseInt(currentCell[0])-parseInt(i+1))+","+parseInt(currentCell[1]))                            
                            }
                            return;                                                        
                        }
                        nextDirection = prevDirection
                        break;                        
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[0])-parseInt(i+1))+","+parseInt(currentCell[1]))
                    }
                    currentCell[0]=parseInt(currentCell[0])-20
                    if(rand<=0.2)//20% go Down
                    {
                        prevDirection = nextDirection                        
                        nextDirection = 1
                    }
                    else if(rand<=0.4){//20% go Up
                        prevDirection = nextDirection                                                
                        nextDirection = 4 
                    } 
                    //60% same direction
                    break;
            case 4: //Up
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[0]))+","+(parseInt(currentCell[1])-parseInt(i+1)))
                        !==-1){
                            nextDirection = prevDirection
                            break;                            
                        }
                    } 
                    if(parseInt(currentCell[1])-20<0){
                        if (parseInt(currentCell[1])+highWayCoordinates.length>=100){
                        for(let i=0;i<parseInt(currentCell[1]);i++){
                            highWayCoordinates.push(parseInt(currentCell[0])+","+(parseInt(currentCell[1])-parseInt(i+1)))                            
                            }
                            return;                                                        
                        }
                        nextDirection = prevDirection
                        break;                        
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[0]))+","+(parseInt(currentCell[1])-parseInt(i+1)))
                    }
                    currentCell[1]=parseInt(currentCell[1])-20
                    if(rand<=0.2)//20% go Left
                    {
                        prevDirection = nextDirection                        
                        nextDirection = 2
                    }
                    else if(rand<=0.4){//20% go Down
                        prevDirection = nextDirection                                                
                        nextDirection = 3 
                    } 
                    //60% same direction
                    break;
            default:
                    break;

        }

    }while(parseInt(currentCell[0])!==0&&parseInt(currentCell[1])!==0&&parseInt(currentCell[1])!==col-1&&parseInt(currentCell[1])!==row-1)

}
var gen_four_hwy=()=>{
    for(let i=0;i<4;i++){
        gen_hwy_cells();        
    }

}
gen_hard_cells();
gen_four_hwy();