param(
    [string]$RemoteName = "official",
    [string]$RemoteBranch = "master",
    [string]$StartCommit = $null,
    [int]$StartCommitSearchDepth = 100
)

# If StartCommit is null, get the last commit on the current branch
if (!$StartCommit) {
    $StartCommit = git rev-parse HEAD
    $found = $false
    for ($currentIndex = 1; $currentIndex -lt $StartCommitSearchDepth; $currentIndex++) {
        $targetMessage = git log --format=%B -n $currentIndex $StartCommit
        $targetMessage = "$targetMessage".Replace("`n", " ")

        # now we should try to see which original commit, this commit
        # been cherry-picked from
        # in the commit message, it should have something like this:
        # (cherry picked from commit <commit-hash>)
        $messageMatches = [regex]::Matches($targetMessage, "cherry picked from commit ([a-f0-9]+)")
        if ($messageMatches.Count -eq 1) {
            $found = $true
            $StartCommit = $messageMatches[0].Groups[1].Value
            break
        }
    }
    
    if (!$found) {
        throw 'Could not find the original commit hash in the commit message'
        exit 1
    }

    Write-Host "Using the last commit on the current branch: $StartCommit" -ForegroundColor Yellow
} else {
    Write-Host "Using provided start commit: $StartCommit" -ForegroundColor Yellow
}

$futureCommits = git rev-list --reverse "$StartCommit..$RemoteName/$RemoteBranch"

if (!$futureCommits) {
    Write-Host "No new commits to cherry-pick, you are all good!" -ForegroundColor Green
    exit 0
}

$totalCommitsDone = 0
$futureCommitsLen = $futureCommits.Length
foreach ($currentCommit in $futureCommits) {
    Write-Host ("Cherry-picking commit: $currentCommit " +
        "($totalCommitsDone / $futureCommitsLen)")

    $gitOutput = (& git cherry-pick $currentCommit -x 2>&1)
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Cherry-pick failed, please resolve the conflicts!" -ForegroundColor Red
        exit 1
    }

    # all good, print the git output
    $totalCommitsDone += 1
    if ($gitOutput -isnot [array]) {
        Write-Host $gitOutput
    } else {
        foreach ($currentOutput in $gitOutput) {
            Write-Host $currentOutput
        }
    }

    # for debugging purposes
    Write-Verbose "done cherry-picking '$currentCommit'"
}