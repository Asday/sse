from fabric.api import (
    cd,
    env,
    require,
    run,
    sudo,
)
from fabric.colors import green

env.use_ssh_config = True

def staging():
    env.host_string = "righttobeoffensive.com"
    env.dir = "/var/www/sse"
    env.git_branch = "develop"

def git_fetch():
    require("dir")

    with cd(env.dir):
        print(green("Fetching."))
        run("git fetch")

def git_reset_hard():
    require("git_branch", "dir")

    with cd(env.dir):
        print(green("Switching branch if needed."))
        run("git checkout {branch}".format(branch=env.git_branch))

        print(green("Updating files to latest version."))
        run("git reset --hard origin/{branch}".format(branch=env.git_branch))

def update_requirements():
    require("dir")

    with cd(env.dir):
        print(green("Updating requirements."))
        run(". env/bin/activate && pip install -r requirements_deploy.txt")

def reload_supervisor():
    require("dir")

    with cd(env.dir):
        print(green("Updating supervisor config and restarting service"))
        sudo("supervisorctl reread")
        sudo("supervisorctl update")

        sudo("supervisorctl restart sse")

def reload_nginx():
    print(green("Reloading nginx config"))
    sudo("nginx -s reload")

def deploy():
    require("host_string", "user", "dir", "git_branch")

    git_fetch()
    git_reset_hard()

    update_requirements()

    reload_supervisor()

    reload_nginx()
