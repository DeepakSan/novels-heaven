import logo from '../assets/novels-heaven.jpg'
import { Link } from 'react-router-dom';  // Import Link from react-router-dom
import searchpic from '../assets/search-pic.png'
import styles from './navbar.module.css'


function AppNavbar() {
    return (
        <nav className={styles.navbar}>
            <div><img className = {styles.logo} src={logo} alt="logo"></img></div>
            <ul className={styles.navlinks}>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/updated-novels">Novel Updates</Link></li>
                <li><Link to="/search"><img className = {styles.search} src={searchpic} alt="search"></img></Link></li>
            </ul>
            <div>
                <button><Link to="/login">Login</Link></button>
                <button><Link to="/signin">Register</Link></button>
            </div>
        </nav>

    );
}   
export default AppNavbar