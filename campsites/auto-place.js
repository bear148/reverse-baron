function autoPlaceTents() {
    // Get grid dimensions by counting elements
    const totalRows = Array.from(document.querySelectorAll('[id^="nr"]')).length;
    const totalCols = Array.from(document.querySelectorAll('[id^="nb"]')).length;

    // Get row and column requirements and tree positions
    const rowNeeds = Array.from({length: totalRows}, (_, i) => parseInt($("#nr"+i).text()));
    const colNeeds = Array.from({length: totalCols}, (_, i) => parseInt($("#nb"+i).text()));
    const trees = Array.from($(".gridbox.marked3")).map(el => el.id);
    
    let solution = null;

    // Validates if a new tent placement is legal
    function isValid(tents, newTent) {
        // Extract coordinates from tent ID (format: X{num}Y{num})
        const [x, y] = newTent.match(/X(\d+)Y(\d+)/).slice(1).map(n => parseInt(n) - 1);
        
        // Check if row/column limits are exceeded
        const rowCount = tents.filter(t => parseInt(t.match(/Y(\d+)/)[1]) - 1 === y).length;
        const colCount = tents.filter(t => parseInt(t.match(/X(\d+)/)[1]) - 1 === x).length;
        if(rowCount >= rowNeeds[y] || colCount >= colNeeds[x]) return false;
        
        // Check if new tent is adjacent to any existing tent
        return !tents.some(tent => {
            const [tx, ty] = tent.match(/X(\d+)Y(\d+)/).slice(1).map(Number);
            const [nx, ny] = newTent.match(/X(\d+)Y(\d+)/).slice(1).map(Number);
            return Math.abs(tx-nx) <= 1 && Math.abs(ty-ny) <= 1;
        });
    }

    // Recursive backtracking to find valid tent placements
    function solve(index, currentTents, usedTrees) {
        if(solution || index >= trees.length) {
            // Check if current solution satisfies all row/col requirements
            const isComplete = rowNeeds.every((need, r) => 
                currentTents.filter(t => parseInt(t.match(/Y(\d+)/)[1]) - 1 === r).length === need) &&
                colNeeds.every((need, c) => 
                    currentTents.filter(t => parseInt(t.match(/X(\d+)/)[1]) - 1 === c).length === need);
            
            if(isComplete) solution = [...currentTents];
            return;
        }

        // Get current tree coordinates
        const [x, y] = trees[index].match(/X(\d+)Y(\d+)/).slice(1).map(Number);
        
        // Try placing tents in adjacent squares
        [[x-1,y], [x+1,y], [x,y-1], [x,y+1]].forEach(([nx,ny]) => {
            if(nx < 1 || ny < 1 || nx > totalCols || ny > totalRows) return;
            
            const tentPos = `X${nx}Y${ny}`;
            if(!usedTrees.has(tentPos) && isValid(currentTents, tentPos)) {
                currentTents.push(tentPos);
                usedTrees.add(tentPos);
                solve(index + 1, currentTents, usedTrees);
                currentTents.pop();
                usedTrees.delete(tentPos);
            }
        });
    }

    // Start solving and update UI if solution found
    solve(0, [], new Set());
    if(solution) {
        solution.forEach(tent => $("#"+tent).removeClass("marked2 marked1_error").addClass("marked1"));
        refigureGrid(0);
    }
}