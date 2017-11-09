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

var determine_direction=(direction,dirArray)=>{
    const dirConfig =[[2,3,4],[1,3,4],[1,2,4],[1,2,3]]
    if(dirArray.length==3)return 0
    if(dirArray.length==2){
      let diff = dirConfig[direction].filter(x => dirArray.indexOf(x) < 0 );
      return diff[0]
    }else{
      let diff = dirConfig[direction].filter(x => dirArray.indexOf(x) < 0 );
      return Math.random()<0.5?
       diff[0]:
       diff[1]
    }


}

var gen_hwy_cells=()=>{
    let xCor = getRandomInt(0,col)
    let yCor = getRandomInt(0,row)
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
        startingCell=[col-1,yCor]
        nextDirection=3// 3 : next move Left
    }
    else{
        startingCell=[xCor,row-1]
        nextDirection=4// 4:  next move Up
    }
    //console.log("prev length",highWayCoordinates.length)
    var prevLength = highWayCoordinates.length
    var collisionFlag=false
    var currentCell=startingCell
    highWayCoordinates.push(parseInt(currentCell[1])+","+parseInt(currentCell[0]))
    var prevDirection = nextDirection
    var direction=[]
    var counter=0;
    do{

        counter++;
        if(counter>300) break;
        rand = Math.random()
        switch (nextDirection){
            case 1://prev Down
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[1])+parseInt(i+1))+","+(parseInt(currentCell[0])))
                        !==-1){
                            // console.log("Down collision at ",(parseInt(currentCell[1])+parseInt(i+1))+","+(parseInt(currentCell[0])))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[1])+20>= row-1){
                        if (row-1-parseInt(currentCell[1])+highWayCoordinates.length-prevLength>=100){
                            // console.log("near bound",row-1-parseInt(currentCell[1])+highWayCoordinates.length-prevLength)
                        for(let i=0;i<row-1-parseInt(currentCell[1]);i++){
                            highWayCoordinates.push((parseInt(currentCell[1])+parseInt(i+1))+","+(parseInt(currentCell[0])))
                            }
                            // //console.log("Down hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[1])+parseInt(i+1))+","+(parseInt(currentCell[0])))
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
                    direction=[]
                    break;
            case 2://Right
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf(parseInt(currentCell[1])+","+(parseInt(currentCell[0])+parseInt(i+1)))
                        !==-1){
                            //console.log("Right collision at ",parseInt(currentCell[1])+","+(parseInt(currentCell[0])+parseInt(i+1)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[0])+20>= col-1){

                        if (col-1-parseInt(currentCell[0])+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",col-1-parseInt(currentCell[0])+highWayCoordinates.length-prevLength)
                        for(let i=0;i<col-1-parseInt(currentCell[0]);i++){
                            highWayCoordinates.push(parseInt(currentCell[1])+","+(parseInt(currentCell[0])+parseInt(i+1)))
                            }
                            //console.log("Right hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push(parseInt(currentCell[1])+","+(parseInt(currentCell[0])+parseInt(i+1)))
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
                    direction=[]
                    break;
            case 3://Left
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf(parseInt(currentCell[1])+","+(parseInt(currentCell[0])-parseInt(i+1)))
                        !==-1){
                            //console.log("Left collision at ",parseInt(currentCell[1])+","+(parseInt(currentCell[0])-parseInt(i+1)))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[0])-20<=0){
                        if (parseInt(currentCell[0])+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",parseInt(currentCell[0])+highWayCoordinates.length-prevLength)
                        for(let i=0;i<parseInt(currentCell[0]);i++){
                            highWayCoordinates.push(parseInt(currentCell[1])+","+(parseInt(currentCell[0])-parseInt(i+1)))
                            }
                            //console.log("Left hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true ;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push(parseInt(currentCell[1])+","+(parseInt(currentCell[0])-parseInt(i+1)))
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
                    direction=[]
                    break;
            case 4: //Up
                    for(let i=0;i<20;i++){
                        if(highWayCoordinates.indexOf((parseInt(currentCell[1])-parseInt(i+1))+","+(parseInt(currentCell[0])))
                        !==-1){
                            //console.log("Up collision at ",(parseInt(currentCell[1])-parseInt(i+1))+","+(parseInt(currentCell[0])))
                            direction.push(nextDirection)
                            nextDirection=determine_direction(nextDirection-1,direction)
                            collisionFlag=true
                            break;
                        }
                    }
                    if(collisionFlag){
                      collisionFlag=false
                      break;
                    }
                    if(parseInt(currentCell[1])-20<=0){
                        if (parseInt(currentCell[1])+highWayCoordinates.length-prevLength>=100){
                            //console.log("near bound",parseInt(currentCell[1])+highWayCoordinates.length-prevLength)
                        for(let i=0;i<parseInt(currentCell[1]);i++){
                            highWayCoordinates.push((parseInt(currentCell[1])-parseInt(i+1))+","+parseInt(currentCell[0]))
                            }
                            //console.log("Up hit bound",highWayCoordinates[highWayCoordinates.length-1])
                            return true;
                        }
                        direction.push(nextDirection)
                        nextDirection=determine_direction(nextDirection-1,direction)
                        break;
                    }
                    for(let i=0;i<20;i++){
                        highWayCoordinates.push((parseInt(currentCell[1])-parseInt(i+1))+","+(parseInt(currentCell[0])))
                    }
                    currentCell[1]=parseInt(currentCell[1])-20
                    if(rand<=0.2)//20% go Right
                    {
                        prevDirection = nextDirection
                        nextDirection = 2
                    }
                    else if(rand<=0.4){//20% go Left
                        prevDirection = nextDirection
                        nextDirection = 3
                    }
                    direction=[]
                    break;
            default:
                    highWayCoordinates=highWayCoordinates.slice(0,prevLength)
                    return false
                    break;

        }

    }while(parseInt(currentCell[0])!==0&&parseInt(currentCell[1])!==0&&parseInt(currentCell[0])!==col-1&&parseInt(currentCell[1])!==row-1)
    if(startingCell === currentCell) {
      highWayCoordinates=highWayCoordinates.slice(0,prevLength)
      return false//need redo whole process
    }
    return true
}
export var gen_four_hwy=()=>{
    let flag = true,c=0

    while(flag){
      flag=false
      for(let i=0;i<4;i++){
          let result= gen_hwy_cells();
          if(result===false)i--
          c++
          if(c>20){
            flag=true
            break;
          };
      }
    }

}
gen_hard_cells();
