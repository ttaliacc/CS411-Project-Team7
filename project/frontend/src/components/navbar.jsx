import React, { Component } from "react";
import "../CSS/homepage.css";

const NavBar = () => (
  <ul>
    <li>
      <a href="default.asp">Home</a>
    </li>
    <li>
      <a href="contact.asp">Contact</a>
    </li>
    <li>
      <a href="about.asp">About</a>
    </li>
    <li style={{ float: "right" }}>
      <a href="about.asp">
        <i class="gg-profile"></i>
      </a>
    </li>
    <li style={{ float: "right" }}>
      <a href="about.asp">Login</a>
    </li>
    <li style={{ float: "right" }}>
      <a href="about.asp">Sign In</a>
    </li>
  </ul>
);

export default NavBar;
