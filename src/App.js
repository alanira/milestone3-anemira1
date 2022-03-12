// Add a state variable (useState) to the App component
// for the fun fact currently being displayed.
//Its initial value can just be an empty string.
//Make sure this variable is referenced
//somewhere in your App component’s return statement (i.e. it renders somewhere on the page).

import {useState, useEffect} from 'react';

// function Button() { // separate component for button
//   return (
//     <button onClick = {handleClick()}>Click me!</button>
//     // <button onClick = {() anon.function handleClick => {variable}>Click me!</button>
//     //modified from
//     // <button onClick = {() => {bandName = "The Wonder Months"}}>Click me!</button>
//   );
// }

function App() {
  
  //const [fact, setFact] = useState("");
  const [comment, setComment] = useState([]);

  useEffect(() => {
    fetch("/display_fact", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data);
      setComment(data.comment);
      

    })

  });
  
return (
  <div>

  <center>
      <h2>Your reviews:</h2>
      <table>
        {comment && comment.map((comment) =>
          <tr>
            <tb><b>Movie ID: {comment.movie_id}</b></tb>&nbsp;
            <tb><input type="text" value={comment.rating} size="3"></input></tb>&nbsp;
            <tb><input type="text" value={comment.comment}></input></tb>&nbsp;
            <button>Delete</button>
          </tr>
        )}
      </table>
      <button>Save Changes</button>
  </center>
  {/* <button onClick = {handleClick}>Click me!</button> */}
  </div>

  );
}

export default App;
