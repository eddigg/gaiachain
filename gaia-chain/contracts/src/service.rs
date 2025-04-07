use cosmwasm_std::{Deps, DepsMut, Env, MessageInfo, Response, StdResult, StdError};
use cosmwasm_schema::{cw_serde, QueryResponses};
use cosmwasm_storage::{singleton, singleton_read, Singleton, ReadonlySingleton};

static SERVICE_KEY: &[u8] = b"service";

#[cw_serde]
pub struct InstantiateMsg {}

#[cw_serde]
pub struct ExecuteMsg {
    pub register_service: Option<RegisterServiceMsg>,
    pub update_service: Option<UpdateServiceMsg>,
}

#[cw_serde]
pub struct RegisterServiceMsg {
    pub name: String,
    pub description: String,
}

#[cw_serde]
pub struct UpdateServiceMsg {
    pub id: u64,
    pub new_description: String,
}

#[cw_serde]
#[derive(QueryResponses)]
pub enum QueryMsg {
    #[returns(ServiceResponse)]
    GetService { id: u64 },
}

#[cw_serde]
pub struct ServiceResponse {
    pub id: u64,
    pub name: String,
    pub description: String,
}

pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    _msg: InstantiateMsg,
) -> StdResult<Response> {
    // Initialize storage
    Ok(Response::default())
}

pub fn execute(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> StdResult<Response> {
    match msg {
        ExecuteMsg::RegisterService { register_service } => {
            if let Some(service) = register_service {
                return try_register_service(deps, env, info, service);
            }
        }
        ExecuteMsg::UpdateService { update_service } => {
            if let Some(service) = update_service {
                return try_update_service(deps, env, info, service);
            }
        }
    }
    Err(StdError::generic_err("Invalid ExecuteMsg"))
}

pub fn try_register_service(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: RegisterServiceMsg,
) -> StdResult<Response> {
    let mut service_store = singleton::<Vec<ServiceResponse>>(deps.storage, SERVICE_KEY);
    let mut services = service_store.load().unwrap_or_default();
    let id = services.len() as u64 + 1;

    let new_service = ServiceResponse {
        id,
        name: msg.name,
        description: msg.description,
    };
    services.push(new_service);

    service_store.save(&services)?;

    Ok(Response::new()
        .add_attribute("method", "try_register_service")
        .add_attribute("service_id", id.to_string()))
}

pub fn try_update_service(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: UpdateServiceMsg,
) -> StdResult<Response> {
    let mut service_store = singleton::<Vec<ServiceResponse>>(deps.storage, SERVICE_KEY);
    let mut services = service_store.load().unwrap_or_default();

    for service in &mut services {
        if service.id == msg.id {
            service.description = msg.new_description;
            service_store.save(&services)?;
            return Ok(Response::new()
                .add_attribute("method", "try_update_service")
                .add_attribute("service_id", msg.id.to_string()));
        }
    }

    Err(StdError::generic_err("Service not found"))
}

pub fn query(
    deps: Deps,
    _env: Env,
    msg: QueryMsg,
) -> StdResult<ServiceResponse> {
    match msg {
        QueryMsg::GetService { id } => query_service(deps, id),
    }
}

fn query_service(
    deps: Deps,
    id: u64,
) -> StdResult<ServiceResponse> {
    let service_store = singleton_read::<Vec<ServiceResponse>>(deps.storage, SERVICE_KEY);
    let services = service_store.load().unwrap_or_default();

    for service in services {
        if service.id == id {
            return Ok(service);
        }
    }

    Err(StdError::generic_err("Service not found"))
}