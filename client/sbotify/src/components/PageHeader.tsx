import '../stylesheets/PageHeader.css'
import sbotifyLogo from '../assets/sbotify_logo_img.png'

export default function PageHeader() {
  return (
    <div className="page-header">
      <img src={sbotifyLogo} alt="bot"></img>
      <h1>Sbotify</h1>
    </div>
  )
}