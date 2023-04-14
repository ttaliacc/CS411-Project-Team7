import React, { Component } from "react";
import "../CSS/homepage.css";
import NavBar from "./navbar";

<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
/>;

class Homepage extends Component {
  state = {};
  render() {
    return (
      <div>
        <div>
          <NavBar />
        </div>
        <div className="title">
          <h1 id="movie">Movie</h1>
          <h1 id="generator">Generator</h1>
        </div>
        <div className="functionBar">
          <button>Filter</button>
          <button>Random Words</button>
        </div>
        <div className="searchBar">
          <form class="search" action="#">
            <input
              type="text"
              placeholder="Find your movies here..."
              name="search"
            />
            <button type="submit">search</button>
          </form>
        </div>
      </div>
    );
  }
}

export default Homepage;
