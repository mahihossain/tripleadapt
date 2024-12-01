import React, { Component } from 'react'
import Card from '@mui/material/Card';

class User extends Component {
    state = { } 

    handleDifficulty = (u, c) => {
      // return u[c].difficulty
      var x = u.filter(u => String(u.id) === String(c))
      return x[0].difficulty
    }

    currentDate() {
        const current = new Date()
        const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;

        return date
    }

    render() { 
      const { onChange, User, current} = this.props
        return (
        <>
          <div style={{'position' : 'absolute', 'left' : '1%', 'top' : '1%'}}>
            Name:
          </div> 
          <div style={{'position' : 'absolute', 'left' : '35%', 'top' : '1%'}}>
          <label>
            <select value={current} onChange={onChange}>
              { User.map(user => (
                <option value={user.id}>{user.name}</option>
              ))}
            </select>
            </label>
          </div>

          <div style={{'position' : 'absolute', 'left' : '1%', 'top' : '40%'}}>
            Date: 
          </div>

          <div style={{'position' : 'absolute', 'left' : '35%', 'top' : '40%'}}>
            {this.currentDate()}
          </div>

          <div style={{'position' : 'absolute', 'left' : '1%', 'top' : '80%'}}>
            Difficulty:
          </div>

          <div style={{'position' : 'absolute', 'left' : '35%', 'top' : '80%'}}>
            {this.handleDifficulty(User,current)}
          </div>
        </>
        );
    }
}
 
export default User;