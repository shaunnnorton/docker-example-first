let ingredient_fields = document.getElementById('in_container')
let amount_fields = document.getElementById('am_container')
console.log(amount_fields)
for(let i = 0; i<ingredient_fields.children.length; i++){
    ingredient_fields.children[i].addEventListener('input', extendList)
    amount_fields.children[i].addEventListener('input', extendList)
}

function extendList() {
    let all_ingredients = document.querySelectorAll("#ingredients")
    let all_amounts = document.querySelectorAll("#ingredient_amounts")
    let last_item_amount = all_amounts[all_amounts.length - 1]
    let last_item = all_ingredients[all_ingredients.length - 1]
   
   
    if(last_item.value != '' && last_item_amount.value != ''){
        let new_child = document.createElement('input')
        new_child.id = 'ingredients'
        new_child.name = 'ingredients'
        /*new_child.required = true*/
        new_child.type = 'text'
        new_child.classList = "ingredients_inputs"
        new_child.addEventListener('input', extendList)
        ingredient_fields.appendChild(new_child)


        new_child = document.createElement('input')
        new_child.id = 'ingredient_amounts'
        new_child.name = 'ingredient_amounts'
        /*new_child.required = true*/
        new_child.type = 'text'
        /*new_child.classList = "ingredients_inputs"*/
        new_child.addEventListener('input', extendList)
        amount_fields.appendChild(new_child)
    }
}