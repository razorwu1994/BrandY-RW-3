const row = 120,col=160
export var randCoordinates =[]
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
gen_hard_cells();