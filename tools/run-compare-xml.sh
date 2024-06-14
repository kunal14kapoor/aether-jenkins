
rm -fr .test
mkdir -p .test/old/config
mkdir -p .test/old/out
mkdir -p .test/new/config
mkdir -p .test/new/out
cd .test
if [ -e /usr/zuul-env/bin/zuul-cloner ];
then
    /usr/zuul-env/bin/zuul-cloner -m ../tools/run-compare-clonemap.yaml --cache-dir /opt/git https://git.openstack.org openstack-infra/project-config
else
    git clone --depth=1 https://git.openstack.org/openstack-infra/project-config
fi
cp -r project-config/jenkins/jobs/* old/config
cp -r project-config/jenkins/jobs/* new/config
cd ..
GITHEAD=`git rev-parse HEAD`

# First generate output from HEAD~1
git checkout HEAD~1
tox -e compare-xml-old

# Then use that as a reference to compare against HEAD
git checkout $GITHEAD
tox -e compare-xml-new

CHANGED=0
for x in `(cd .test/old/out && find -type f)`
do
    if ! diff -u .test/old/out/$x .test/new/out/$x >/dev/null 2>&1
    then
	CHANGED=1
	echo "============================================================"
	echo $x
	echo "------------------------------------------------------------"
    fi
    diff -u .test/old/out/$x .test/new/out/$x || /bin/true
done

echo
echo "You are in detached HEAD mode. If you are a developer"
echo "and not very familiar with git, you might want to do"
echo "'git checkout branch-name' to go back to your branch."

if [ "$CHANGED" -eq "1" ]; then
    exit 1
fi
exit 0
