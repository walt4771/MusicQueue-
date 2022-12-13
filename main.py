from flask import Flask, request, Response, render_template, redirect, url_for
app = Flask(__name__)

import pafy
import vlc
import time

import threading

# musicQueue = ['https://www.youtube.com/watch?v=Waz8rfdvVsY', 'https://www.youtube.com/watch?v=B-hyHjwGlz4']
musicQueue = []

isMusicPlaying = False

class WebThread(threading.Thread):
    def run(self):
        @app.route('/register')
        def register():
            global musicQueue
        
            url = request.args.get('url', "")
            if 'youtu.be' in url:
                url = 'https://www.youtube.com/watch?v=' + url.split('.be/')[1]
            
            video = pafy.new(url)
            
            m, s = divmod(video.length, 60)
            a = {
                'title' : video.title,
                'author': video.author,
                'length': f'{m:02d}:{s:02d}',

                'url': url
            }
            musicQueue.append(a)
            return redirect(url_for('main'))

        @app.route('/main')
        def main():
            global musicQueue
            
            if len(musicQueue) != 0:
                return render_template('musiclist.html', posts=musicQueue)
            elif len(musicQueue) == 0:
                return render_template('musiclist_empty.html')

        # app.run(host="192.168.0.21" ,port=5000)
        app.run(host="172.18.250.17" , port=5000)
        # app.run(host="172.20.10.2" ,port=5000)
        

class QueueThread(threading.Thread):
    def run(self):
        def playMusic(video):
            best = video.getbest()
            playurl = best.url
            Instance = vlc.Instance("--no-video")
            player = Instance.media_player_new()
            Media = Instance.media_new(playurl)
            Media.get_mrl()
            player.set_media(Media)
            player.play()

        while True :
            global isMusicPlaying
            print(str(len(musicQueue)))
            time.sleep(3)
            if isMusicPlaying is False:
                if len(musicQueue) != 0 :
                    video = pafy.new(musicQueue.pop().get('url'))
                    playMusic(video)
                    time.sleep(video.length)
                    isMusicPlaying = False
        

QueueThread().start()
WebThread().start()
