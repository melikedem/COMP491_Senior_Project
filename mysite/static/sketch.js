let obj_array = [];



function setup() {
  let list = JSON.parse(document.getElementById('json').textContent);
  for (let i = 0; i< list.length; i++){
    let a = JSON.parse(list[i]);
    let obj = new DrawingObject(a.name, a.color, a.size, a.number, 100+ 250 * i, 100, a.strokeArray);
    obj_array.push(obj);
  }

  var canvas = createCanvas(1060,450);
  canvas.parent("sketchholder");
}



function draw() {
    //translate(-275, -175);
  //box(85);
 //  alert(obj.strokeArray)
  for (let i = 0; i< obj_array.length; i++){
    obj_array[i].display();
  }
}


class DrawingObject {
  constructor(name, color, size, number, location_X, location_Y, strokeArray) {
    this.ready= 0;
    this.name =name;
    this.color= color;
    this.size= size;
    this.number= number;
    this.index = 0;
    this.strokeIndex = 0;
    this.location_X = location_X;
    this.location_Y = location_Y;
    this.strokeArray = strokeArray;

  }


    display() {
//alert(this.strokeArray.length);
  for(let i=0; i <= this.strokeArray[this.strokeIndex][0].length; i++){
      let x = this.strokeArray[this.strokeIndex][0][this.index]+this.location_X ;
      x = x * this.size;
      let y = this.strokeArray[this.strokeIndex][1][this.index]+this.location_Y;
      y = y * this.size;
      stroke(this.color);
      if (this.prevx !== undefined) {
        line(this.prevx, this.prevy, x, y);
      }
      this.index++;
      if (this.index === this.strokeArray[this.strokeIndex][0].length) {
      this.strokeIndex++;
      this.prevx = undefined;
      this.prevy = undefined;
      this.index = 0;
      if (this.strokeIndex === this.strokeArray.length) {
        this.strokeArray = undefined;
        this.strokeIndex = 0;
      }
    } else {
      this.prevx = x;
      this.prevy = y;
    }
  }

  }
}