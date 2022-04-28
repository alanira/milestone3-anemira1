import {useState, useEffect} from 'react';


function App() {
  
  const [comment, setComment] = useState([]);
  const [ids, updateIds] = useState([]);
  const [del_ids, updatedel_Ids] =useState([]);

  const deleteComment= (name) =>{  
    let comm = [...comment] 
    // debugger
    comm.splice(comm.indexOf(parseInt(name.value)), 1)
    setComment(comm)
    let idss = [...del_ids]
    idss.push(name.id)
    updatedel_Ids(idss)
    
  }
    
const changeComment = (value) =>{
  let comm = [...comment] // take all comments
  comm[parseInt(value.name)].comment = value.value; // updating the comment 
  setComment(comm) // put updated comment back to var comment using setComment function
  let idss = [...ids]
  idss.push(value.id)
  updateIds(idss)

}

const updateRating = (value) =>{
  // debugger
  let comm = [...comment] 
  comm[parseInt(value.name)].rating = value.value;
  setComment(comm)
  let idss = [...ids]
  idss.push(value.id)
  updateIds(idss)
}
  


  useEffect(() => {// componentdidmount
    let user = localStorage.getItem("username")
    fetch(`/display_fact?user=${user}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }

    })
    
  .then(response => response.json())
  .then(data => {
    // debugger; 
    setComment(data.comment);
    console.log(data)});

  },[]);

  const saveChanges = () => {
    fetch("/update_comments", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body:JSON.stringify({"ids": ids, 
                          "del_ids": del_ids,
                          "data": comment})
    })
    
  .then(response => response.json())
  .then(data => {
    // debugger; 
    alert(data.msg)
    console.log(data)});
  }
  
return (
  <div className="container">
    <h2 className="d-flex justify-content-center">Your Reviews</h2>
    {comment.length===0 &&
        <h2 className="d-flex justify-content-center">No reviews yet. Write Your First rewiew!!</h2>
      }
    
{comment && comment.map((comment,idx) =>
<div className = "p-3" key={idx} >
<form className="row">
  <div className="form-group col">
  <b>Movie ID: {comment.movie_id}</b><br/>
    <label htmlFor="exampleInputEmail1">Rating</label>
    <select className="form-control" 
    id={comment.id}
    value={comment.rating} 
    name={idx}
    onChange={(event)=>updateRating(event.target)}>
      <option>1</option>
      <option>2</option>
      <option>3</option>
      <option>4</option>
      <option>5</option>
    </select>
  </div>
  <div className="form-group col">
    <label htmlFor="Textarea1">Comment</label>
    <textarea className="form-control" 
    id={comment.id}
    rows="3" 
    name={idx}
    onChange={event => changeComment(event.target)}
    value={comment.comment}
    ></textarea>
  </div>
  
</form>
<div className="mx-auto">
<button type="button" className="btn btn-danger" name={idx} id={comment.id} onClick={(event) =>deleteComment(event.target)}>Delete</button>
</div>
</div>
)}
  
      
      
      <div className="d-flex justify-content-center" style={{Width:"50%"}}>
      <button type="button" className="btn btn-primary btn-lg btn-block" onClick={saveChanges}>Save</button>
      </div>
 
  
  </div>

  );
}

export default App;
