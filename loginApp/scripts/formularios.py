def procesar_form(form, sol):
    if form.is_valid():
        sol.campos_sol = form.cleaned_data
        if "fecha_expiracion" in sol.campos_sol and sol.campos_sol["fecha_expiracion"] is not None:
            # Arreglar el formato de fecha
            sol.campos_sol["fecha_expiracion"] = sol.campos_sol["fecha_expiracion"].strftime("%Y-%m-%d")
        else:
            del(sol.campos_sol["fecha_expiracion"])
        if form.files:
            sol.adjunto_sol = form.files[f'{sol.tipo_sol}-adjunto']
            del(sol.campos_sol["adjunto"])
        return sol
    
def revision_form(sol, lista_sol):
    tipo_sol, campos_sol = sol.tipo_sol, sol.campos_sol
    #Cambiar a un switch a futuro si otros tipos de solicitudes requieren mas verificaciones
    if tipo_sol == "Servicio VPN":
        for s in lista_sol:
            campos_sol_alojado = s.campos_sol
            if campos_sol["usuario"] == campos_sol_alojado["usuario"]:
                return False
    return True