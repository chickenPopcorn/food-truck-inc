# Development Workflow

Use any editor you like, but **follow these steps for `git`**.

## How & Where to Code

The high-level overview: we use `branch`es, pull-requests, and travis-ci.org's
automatic `make test` integration.

### Code in Branches

Say you're working on `fancyNewBuiltin()`

**tl;dr** _new_ branch for _every_ feature, `git diff` before committing!!

1. `git checkout -b [yourhandle]-add-fancy-new-builtin`
 - tip: make sure `git branch` shows that ^ worked
2. before creating `fancyNewBuiltin()`, **write tests for it**:
  - [write & save new tests in a text editor](../src/#writing-tests) for your `fancyNewBuiltin()`
  - ensure it `FAIL`s, since you haven't coded yet
  - commit tests: `git add ./tests/your-new /tests/test-files`
  - share tests: `git push origin [yourhandle]-add-fancy-new-builtin`
3. [open pull request](https://help.github.com/articles/creating-a-pull-request/) for `[yourhandle]-add-fancy-new-builtin`
4. **do in loop**, until tests `PASS`:
  - write code for `fancyNewBuiltin()`
  - save in your text editor
  - `make test` to see what happened
  - double-check `git diff` makes sense to you (fix now otherwise)
  - if you have small changes you like: `git add file/you/changed && git commit`
5. repeat step 4 until `make test` passes
6. **assign** your pull-request to someone for a last-minute check
 - address (ie: git `commit` and `push`) problems they point out
 - fix (ie: git `commit` and `push`) [anything your pull-request shows broken](https://cloud.githubusercontent.com/assets/156228/14194012/fad8247a-f777-11e5-8a67-d5e23c3cd2d9.png)
7. click ["merge your pull request"](https://help.github.com/articles/merging-a-pull-request/) button
8. **cleanup on laptop** before moving onto next thing:
  - fetch your new merge: `git checkout master && git fetch --all && git pull origin master`
  - delete yor laptop's branch: `git branch -d [yourhandle]-add-fancy-new-builtin`

### Collaborating in Branches

Say A is working on "cool-feature". B want to use A's work:

**Q**: How do I work with someone else's in-progress branch, `A-cool-feature`?

**A**:

1. ensure you're in a clean repo: `git status` _(should output nothing)_
2. ensure your laptop's updated: `git fetch --all`
3. **start your own branch**, eg: for `B-cool-feature` do:
   `git checkout -b B-cool-feature origin/A-cool-feature`

Now just continue with a normal ["Code in Branches"](#code-in-branches) process.

**Q**: I'm A, how do I get B's fork back into my branch? **A**:

1. ensure you're in a clean repo: `git status` _(should output nothing)_
2. ensure your laptop's updated: `git fetch --all`
3. ensure your'e in original branch: `git branch` outputs  `A-cool-feature`
4. Merge the fork of your branch back in: `git merge origin/B-cool-feature`

It helps if you're talking to each other, of course, to avoid confusion :)

**Q**: How to see the difference for a file "main.c" between now and two commits back?

**A**:
  ```
  $ git diff HEAD^^ HEAD main.c
  $ git diff HEAD^^..HEAD -- main.c
  $ git diff HEAD~2 HEAD -- main.c
  ```

**Q**: I read this whole doc, and I'm stuck on something `git` related :(

**A**: No worries! Share [Pastie](https://dpaste.de) of these, for debugging:

  ```sh
  $ git rev-list --format=%B --max-count=1 HEAD
  $ git branch -v --all
  $ git status
  $ git diff
  ```
