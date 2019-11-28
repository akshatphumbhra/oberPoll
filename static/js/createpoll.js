// css style to align text to the center of it's container
var Align = {
  textAlign: 'center'
};

var pollForm = React.createClass({
//Sets up initial state of component
//Title stores the poll question, options is an array that holds each option
  getInitialState: function(){
    return {title: '', option: '', options: [{name: "Akshat"}, {name:"Oishani"}]}
  },

  //functions that handle live changes to the form
  handleTitleChange: function(e){
    //change title as the user types
    this.setState({title: e.target.value});
  },

  handleOptionChange: function(e){
    this.setState({option: e.target.value});
  },

  handleOptionAdd: function(e){
    //update poll options and reset options to an empty string
    this.setState({
    options: this.state.options.concat({name: this.state.option}),
    option: ''
    });
  },

  handleSubmit: function(e){
    //TODO handle form submit
    e.preventDefault();
  },

  render: function(){
    return (
      <div>
      <form id="poll_form" className="form-signin" onSubmit={this.handleSubmit}>
        <h2 className="form-signin-heading" style={Align}>Create a poll</h2>

        <div className="form-group has-success">
          <label htmlFor="title" className="sr-only">Title</label>
          <input type="text" id="title" name="title" className="form-control" placeholder="Title" onChange={this.handleTitleChange} required autoFocus />
        </div>

        <div className="form-group has-success">
          <label htmlFor="option" className="sr-only">Option</label>
          <input type="text" id="option" name="option" className="form-control" placeholder="Option" onChange={this.handleOptionChange}  required autoFocus />
        </div>

        <div className="row form-group">
          <button className="btn btn-lg btn-success btn-block" onClick={this.handleOptionAdd}>Add option</button>
          <button className="btn btn-lg btn-success btn-block" type="submit">Save poll</button>
        </div>
        <br />
      </form>

      <h3 style={Align}>Live Preview</h3>
      <LivePreview options={this.state.options} />
    </div>
  );
  }
});

//It renders a live preview of what the form would look like
var LivePreview = React.createClass({
  render: function(){
//Mapping a function that converts all options to radio buttons
    var options = this.props.options.map(function(option){ //props (properties) is used to pass data from a component to its parent
      return (
        <div key={option.name}>
         <input name={option.name} type="radio" value={option.name} /> {option.name}
         <br />
       </div>
     );
   });

   return(
     <div className="panel panel-success">
       <div className="panel-heading">
         <h4>Alex iwobi vs Dele Alli</h4>
       </div>
       <div className="panel-body">
         <form>
           {options}
           <br />
           <button type="submit" className="btn btn-success btn-outline hvr-grow">Vote!</button>
         </form>
       </div>
     </div>
   )
  }
});

ReactDOM.render(
  <div>
  <pollForm />
</div>,
document.getElementById('form_container')
);
