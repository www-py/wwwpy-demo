from wwwpy.remote.widget import Widget


class WelcomeWidget(Widget):
    def __init__(self):
        super().__init__(_html)



# the following message is displayed when the user opens the app
# it is in html/boostrap format
# the content you are going to write is
# welcome the user to wwwpy-demo and give the link to
# 'https://github.com/www-py/wwwpy-demo'
# Then you are going to tell the user that everything you see is written in python
# language=HTML
_html = """<div class="container">
    <div class="row">
        <div class="col">
            <h1>Welcome to wwwpy-demo</h1>
            <p>
                This is a demo of wwwpy. It is a python library that allows you to write web apps in python.
                It is based on <a href="https://github.com/www-py/wwwpy">wwwpy</a>.
                <br>
                You can get the source code of this demo <a href="https://github.com/www-py/wwwpy-demo">here</a>.
                
            </p>
            <p>
                Everything you see here is written in python.
                The UI use the popular CSS Framework <a href="https://getbootstrap.com/">Bootstrap</a>.               
            </p>
        </div>
    </div>
</div>
"""
